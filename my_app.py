from shiny import App,ui, render
from datetime import date,timedelta
import pandas as pd
from xhtml2pdf import pisa
from io import BytesIO

job=pd.DataFrame({"Sector":["IT","Marketing","HR"],
                  "id":["it","markt","hr"],
                  "Site of Employement":["Paris","London","New York"],
    "Remote work frequency":["Full-remote","Never","Two days a week"],
    "Working Hours per week":["45 hours","48 hours","42 hours"],
    "Salary":["27€ per hour","1062£ per week","552$ per workday"]
                                                                        })

job_to_id={
            "it": "Junior Data Analyst",
            "markt": "Digital Marketing Specialist",
            "hr": "Human Resources Coordinator"
        }

desc_to_id={"it":"We expect you to supports data-driven decision-making by collecting, cleaning, and organizing datasets. They create basic reports, build visualizations, and assist senior analysts with statistical analysis and business insights. This role requires strong attention to detail, proficiency in tools like Excel, SQL, or Python, and a curiosity for understanding patterns in data.",
"markt":"We expect you to develops and executes online marketing campaigns across channels such as social media, email, SEO, and paid advertising. They analyze performance metrics, optimize content for engagement, and help grow brand visibility. The role blends creativity with analytical skills to improve customer acquisition and digital presence",
"hr":"We expect you to supports daily HR operations, including recruitment scheduling, onboarding, employee record management, and internal communication. They ensure smooth administrative processes, assist employees with HR-related inquiries, and help maintain compliance with company policies. This role requires strong organizational and interpersonal skills."
}

remote_to_id={
    "it":"The Employee is permitted to work remotely on a regular basis. Unless otherwise required for business needs, the Employee may perform their duties from home or another approved remote location.",
    "markt":"The Employee is required to perform all duties on-site at the company's premises. Remote work is not permitted under this Agreement.",
    "hr":"The Employee is allowed to work remotely up to two days per week, subject to prior scheduling with their manager. The remaining working days must be performed on-site."
}

company=pd.DataFrame({"id":["it","markt","hr"],
    "Address":["5 Avenue Anatole France, 75007 Paris",
    "Westminster, London SW1A 0AA, ",
    "Liberty Island, New York, NY 10004"],
                    "Name":["Business France","Business UK","Business US"]
})

app_ui = ui.page_navbar(
ui.nav_panel("Jobs Informations",
ui.page_fluid(
ui.input_radio_buttons(
        id="job",
        label="Select the job",
        choices=job_to_id
    ),
    ui.output_data_frame("job_table")
)#End job's Page
),#End job's panel
ui.nav_panel("Enter Employee's Informations",
ui.page_fluid(

    ui.input_text(
        id="text_fname",
        label="First Name",
        placeholder="Enter first name",
        value="John"
    ),

    ui.input_text(
        id="text_lname",
        label="Last Name",
        placeholder="Enter last name",
        value="Doe"
    ),

    ui.input_text(
        id="text_address",
        label="Address",
        placeholder="Enter Adress",
        value="742 Evergreen Terrace, Springfield"
    ),

    ui.input_radio_buttons(
        id="mode",
        label="Contract Type",
        choices={
            "range": "Fixed-term contract",
            "noend": "Permanent contract"
        }
    ),

    ui.panel_conditional(
        "input.mode === 'range'",
        ui.input_date_range(
            id="date_range",
            label="Contract Duration",
            start=date.today(),
            end =date.today()+timedelta(days=1)
        )
    ),

    ui.panel_conditional(
        "input.mode === 'noend'",
        ui.input_date(
            id="starting_date",
            label="Contract Starting Date",
            value=date.today()
        )
    )

)#End Employee's Info Page
),#End Employee's Info panel
ui.nav_panel("Preview of the Contract",
ui.page_fluid(
ui.output_ui("contract"),
ui.download_button("download_pdf", "Download PDF")
)#End Contract Page
)#End Contract panel
)#End Navbar


def server(input, output, session):

    @output
    @render.data_frame
    def job_table():
        df=job[job["id"]==input.job()].drop(columns=["id"]).T.reset_index()
        df.columns=["Field","Job Information"]
        return render.DataTable(df)

    
    def build_html():

        return f""" 
        <html lang="en"> 
        <head> 
            <meta charset="UTF-8"> 
            <style> 
            body {{ font-family: Helvetica, 
            sans-serif; 
            margin: 40px;
                line-height: 1.5;
                font-size: 14px; }} 
                h1, h2 {{ text-align: center; }} 
                h1 {{ text-transform: uppercase;
                font-size: 22px; 
                margin-bottom: 10px; }} 
                h2 {{ text-transform: uppercase;
                    font-size: 16px; 
                margin-top: 30px; 
                text-align: left; }}
                .section {{ margin-top: 15px; }}
            </style>
            </head>
        <body>
        <div class="section">
            <h1>Employment Contract</h1>
        </div>
        <div class="section">
            <h2>1. Employement Agreement</h2>
            <p>
                This Employment Agreement is made between <strong>
                {company[company["id"]==input.job()]["Name"].iloc[0]} </strong>
                located at <strong>
                {company[company["id"]==input.job()]["Address"].iloc[0]}
                </strong> 
                (“Employer”), and <strong>
                {input.text_fname()} {input.text_lname()}</strong>,
                residing at <strong>{input.text_address()}</strong> 
                (“Employee”). 
                This Agreement becomes effective on 
                <strong>{input.starting_date().strftime("%d/%m/%y") 
                if input.mode() =="noend" 
                else input.date_range()[0].strftime("%d/%m/%y")+
                " </strong>until<strong> "+input.date_range()[1].strftime("%d/%m/%y")}
                </strong>
            </p>
        </div>
        <div class="section">
            <h2>2. Position and Duties</h2>
            <p> 
                The Employer agrees to employ the Employee as <strong>
                {job_to_id.get(input.job())}</strong>. The Employee agrees to 
                perform all duties reasonably assigned to this position and 
                to comply with all company policies, procedures, 
                and standards of conduct. {desc_to_id.get(input.job())}
            </p>
        </div>
        <div class="section">
            <h2>3. Working Hours</h2>
            <p>
                The Employee's normal working schedule shall be <strong>
                {job[job["id"]==input.job()]["Working Hours per week"].iloc[0]}
                </strong> per week subject to operational needs. Additional hours 
                may be required depending on workload and business requirements,
                in accordance with applicable laws. {remote_to_id.get(input.job())}
            </p>
        </div>
        <div class="section">
            <h2>4. Compensation</h2>
            <p>
                The Employee will receive a salary of <strong>
                {job[job["id"]==input.job()]["Salary"].iloc[0]}</strong>
                , payable in accordance with the Employer's standard 
                payroll schedule. Any bonuses or incentives are discretionary 
                unless otherwise stated in writing.
            </p>
        </div>
        <div class="section">
            <h2>5. Entire Agreement</h2>
            <p>
                This document constitutes the entire agreement between the parties 
                and supersedes all prior discussions or understandings.
            </p>
        </div>
        <table class="signatures">
            <tr>
                <td>
                    <strong>For the Employer</strong><br><br><br><br><br>
                    Signature: ___________________________<br>
                    Name: {company[company["id"]==input.job()]["Name"].iloc[0]}<br>
                </td>
                <td>
                    <strong>For the Employee</strong><br><br><br><br><br>
                    Signature: ___________________________<br>
                    Name: {input.text_fname()} {input.text_lname()}
                </td>
            </tr>
        </table>
        </body>
        </html>

        """
    @output
    @render.ui 
    def contract():
        html=build_html()
        return ui.HTML(html)

    @output 
    @render.download(filename="output.pdf") 
    def download_pdf():
        html=build_html()
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
        if pisa_status.err: 
            yield b"PDF generation failed" 
            return 
        pdf_buffer.seek(0)
        yield pdf_buffer.read()

app = App(app_ui, server)
