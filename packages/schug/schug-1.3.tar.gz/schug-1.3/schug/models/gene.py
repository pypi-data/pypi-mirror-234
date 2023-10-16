from typing import TYPE_CHECKING, List, Literal, Optional

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import validator
from sqlmodel import Field, Relationship

from .common import CoordBase

if TYPE_CHECKING:
    from .transcript import Transcript, TranscriptRead


class GeneBase(CoordBase):
    hgnc_id: Optional[int]
    primary_symbol: Optional[str]


class Gene(GeneBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transcripts: List["Transcript"] = Relationship(back_populates="gene")


class GeneRead(GeneBase):
    id: int


class GeneCreate(GeneBase):
    pass


class GeneReadWithTranscript(GeneRead):
    transcripts: List["TranscriptRead"] = []


class EnsemblGene(BaseModel):
    chromosome: str = PydanticField(..., alias="Chromosome/scaffold name")
    resource_id: str = PydanticField(..., alias="Gene stable ID")
    start: int = PydanticField(..., alias="Gene start (bp)")
    end: int = PydanticField(..., alias="Gene end (bp)")
    genome_build: Optional[str]
    resource: str = "Ensembl"
    hgnc_symbol: Optional[str] = PydanticField(None, alias="HGNC symbol")
    hgnc_id: Optional[int] = PydanticField(None, alias="HGNC ID")

    @validator("*", pre=True)
    def convert_to_none(cls, v):
        if v == "":
            return None
        return v

    @validator("hgnc_id", pre=True)
    def modify_id(cls, v):
        if type(v) != int:
            return v.replace("HGNC:", "")
        return v


class HgncGene(BaseModel):
    gene_id: str = PydanticField(..., alias="Gene stable ID")
    ensembl_gene_id: str
    entrez_id: int
    hgnc_symbol: str = PydanticField(None, alias="HGNC symbol")
    hgnc_id: str
    ccds_id: Optional[str] = None
    short_description: str = PydanticField(None, alias="alias_name")
    alias_symbol: str

    aliases: List[str] = []

    @validator("gene_id", always=True)
    def set_alias_symbols(cls, _, values: dict):
        return values["alias_symbols"].split("|")


def into_gene(ensembl_gene: EnsemblGene) -> Gene:
    """Convert EnsemblGene to Gene"""
    return Gene(
        chromosome=ensembl_gene.chromosome,
        start=ensembl_gene.start,
        end=ensembl_gene.end,
        genome_build=ensembl_gene.genome_build,
        hgnc_id=ensembl_gene.hgnc_id,
        primary_symbol=ensembl_gene.hgnc_symbol,
        resource_id=ensembl_gene.resource_id,
        resource=ensembl_gene.resource,
    )


"""
{
    "hgnc_id": "HGNC:15766",
    "homeodb": "8666",
    "horde_id": None,
    "imgt": None,
    "intermediate_filament_db": None,
    "iuphar": None,
    "kznf_gene_catalog": None,
    "lncrnadb": None,
    "location": "20q13.13",
    "location_sortable": "20q13.13",
    "locus_group": "protein-coding gene",
    "locus_type": "gene with protein product",
    "lsdb": "",
    "mamit-trnadb": None,
    "merops": None,
    "mgd_id": "MGI:1338758",
    "mirbase": "",
    "name": "activity dependent neuroprotector homeobox",
    "omim_id": "611386",
    "orphanet": "406010",
    "prev_name": "activity-dependent neuroprotector",
    "prev_symbol": "",
    "pseudogene.org": None,
    "pubmed_id": "9872452|11013255",
    "refseq_accession": "NM_181442",
    "rgd_id": "RGD:71030",
    "rna_central_ids": None,
    "snornabase": "",
    "status": "Approved",
    "symbol": "ADNP",
    "ucsc_id": "uc002xvt.3",
    "uniprot_ids": "Q9H2P0",
    "vega_id": "OTTHUMG00000032737",
}
"""
