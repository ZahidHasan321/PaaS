from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Index Page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ======== Problem 1: Generate Even Numbers ========
@app.get("/problem1", response_class=HTMLResponse)
async def problem1_get(request: Request):
    return templates.TemplateResponse("problem1.html", {"request": request})


@app.post("/problem1", response_class=HTMLResponse)
async def problem1_post(
    request: Request,
    n: int = Form(..., gt=0, description="Number of even numbers to generate"),
):
    try:
        even_numbers = [2 * i for i in range(n)]
        return templates.TemplateResponse(
            "problem1.html",
            {"request": request, "result": f"First {n} even numbers: {even_numbers}"},
        )
    except Exception as e:
        return templates.TemplateResponse(
            "problem1.html", {"request": request, "error": f"Error: {str(e)}"}
        )


# ======== Problem 2: Matrix Multiplication ========
@app.get("/problem2", response_class=HTMLResponse)
async def problem2_get(request: Request):
    return templates.TemplateResponse("problem2.html", {"request": request})


def parse_matrix(matrix_str: str):
    return [
        [float(num.strip()) for num in row.split(",")]
        for row in matrix_str.strip().split("\n")
        if row
    ]


@app.post("/problem2", response_class=HTMLResponse)
async def problem2_post(
    request: Request, matrix_a: str = Form(...), matrix_b: str = Form(...)
):
    try:
        a = parse_matrix(matrix_a)
        b = parse_matrix(matrix_b)

        np_a = np.array(a)
        np_b = np.array(b)

        if np_a.shape[1] != np_b.shape[0]:
            raise ValueError("Matrix dimensions incompatible for multiplication")

        result = np.matmul(np_a, np_b)

        return templates.TemplateResponse(
            "problem2.html",
            {
                "request": request,
                "result": f"Result:\n{np.array_str(result, precision=2)}",
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "problem2.html", {"request": request, "error": f"Error: {str(e)}"}
        )


# ======== Problem 4: Nth Largest Number ========
@app.get("/problem4", response_class=HTMLResponse)
async def problem4_get(request: Request):
    return templates.TemplateResponse("problem4.html", {"request": request})


@app.post("/problem4", response_class=HTMLResponse)
async def problem4_post(
    request: Request, numbers: str = Form(...), n: int = Form(..., gt=0)
):
    try:
        num_list = [float(num.strip()) for num in numbers.split(",")]
        unique_nums = sorted(list(set(num_list)), reverse=True)

        if n > len(unique_nums):
            raise ValueError("n exceeds number of unique elements")

        return templates.TemplateResponse(
            "problem4.html",
            {
                "request": request,
                "result": f"{n}th largest number is {unique_nums[n - 1]}",
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "problem4.html", {"request": request, "error": f"Error: {str(e)}"}
        )


# ======== Placeholder Routes ========
@app.get("/problem3", response_class=HTMLResponse)
async def problem3_get(request: Request):
    return templates.TemplateResponse("problem3.html", {"request": request})


@app.get("/problem5", response_class=HTMLResponse)
async def problem5_get(request: Request):
    return templates.TemplateResponse("problem5.html", {"request": request})
