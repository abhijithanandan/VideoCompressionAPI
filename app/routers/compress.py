import subprocess

from fastapi import APIRouter

router = APIRouter(
    prefix="/compress",
    tags=["compress"]
)


@router.get("/")
def compress_video():
    input_path = r""
    output_path = r""
    handbrake_commands = [r"../../HandBrake/build/HandBrakeCLI", "-i", f"{input_path}", "-o", f"{output_path}", "-e", "x264"]
    subprocess.run(handbrake_commands, shell=True)
