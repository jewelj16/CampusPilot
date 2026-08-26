"""
Phase 1 has no auth yet (that's M1 in the roadmap). Every request is
treated as coming from a single seeded student so the registration flow
end-to-end (list meals -> register -> see it reflected) can be built and
demoed honestly, without faking a login screen that doesn't do anything.

When M1 lands, this becomes a real `get_current_student` FastAPI
dependency backed by a JWT, and every route below keeps working
unchanged — it already depends on `get_current_student_id`.
"""
from typing import Annotated

from fastapi import Depends

DUMMY_STUDENT_ID = "stu_00001"


def get_current_student_id() -> str:
    return DUMMY_STUDENT_ID


CurrentStudentId = Annotated[str, Depends(get_current_student_id)]
