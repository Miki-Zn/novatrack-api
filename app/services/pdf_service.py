from fpdf import FPDF
from app.models.task import Task
from app.models.project import Project

class PDFReportService:
    def generate_project_report(self, project: Project, tasks: list[Task]) -> bytes:
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, f"Project Report: {project.title}", new_x="LMARGIN", new_y="NEXT", align="C")
        
        pdf.set_font("helvetica", "", 12)
        description = project.description if project.description else "No description provided."
        pdf.cell(0, 10, f"Description: {description}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 10, "", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("helvetica", "B", 12)
        pdf.cell(120, 10, "Task Title", border=1)
        pdf.cell(60, 10, "Status", border=1, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("helvetica", "", 12)
        for task in tasks:
            pdf.cell(120, 10, task.title, border=1)
            pdf.cell(60, 10, task.status.value, border=1, new_x="LMARGIN", new_y="NEXT")

        return pdf.output()