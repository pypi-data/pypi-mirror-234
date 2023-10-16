from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from schug.database.session import get_session
from schug.load.biomart import EnsemblBiomartClient
from schug.load.ensembl import fetch_ensembl_transcripts
from schug.load.fetch_resource import stream_resource
from schug.models import Transcript, TranscriptRead
from schug.models.common import Build
from schug.models.transcript import TranscriptReadWithExons
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=List[TranscriptRead])
def read_transcripts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    transcripts = session.exec(select(Transcript).offset(offset).limit(limit)).all()
    return transcripts


@router.get("/{db_id}", response_model=TranscriptReadWithExons)
def read_transcript_db_id(
    *,
    db_id: int,
    session: Session = Depends(get_session),
):
    transcript = session.get(Transcript, db_id)
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transcript not found"
        )
    return transcript


@router.get("/ensembl_transcripts/", response_class=StreamingResponse)
async def ensembl_transcripts(build: Build):
    """A proxy to the Ensembl Biomart that retrieves transcripts in a specific genome build."""

    ensembl_client: EnsemblBiomartClient = fetch_ensembl_transcripts(build=build)
    url: str = ensembl_client.build_url(xml=ensembl_client.xml)

    return StreamingResponse(stream_resource(url), media_type="text/tsv")
