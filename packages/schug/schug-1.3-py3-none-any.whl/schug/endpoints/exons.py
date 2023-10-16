from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from schug.database.session import get_session
from schug.load.ensembl import fetch_ensembl_exons
from schug.load.fetch_resource import stream_resource
from schug.models import Exon, ExonRead
from schug.models.common import Build
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=List[ExonRead])
def read_exons(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    exons = session.exec(select(Exon).offset(offset).limit(limit)).all()
    return exons


@router.get("/ensembl_exons/", response_class=StreamingResponse)
async def ensembl_exons(build: Build):
    """A proxy to the Ensembl Biomart that retrieves exons in a specific genome build."""

    ensembl_client: EnsemblBiomartClient = fetch_ensembl_exons(build=build)
    url: str = ensembl_client.build_url(xml=ensembl_client.xml)

    return StreamingResponse(stream_resource(url), media_type="text/tsv")
