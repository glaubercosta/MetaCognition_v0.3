from fastapi import APIRouter
from typing import List
from ..models import Evaluation, EvaluationCreate
from ..services import evals_service as svc

router = APIRouter(prefix="/evaluations", tags=["evaluations"])

@router.post("", response_model=Evaluation, status_code=201)
def create_evaluation(ev: EvaluationCreate):
    return svc.create_evaluation(ev)

@router.get("", response_model=List[Evaluation])
def list_evaluations():
    return svc.list_evaluations()
