import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Jenkins CI/CD Pipeline — Presentation Guide & Task Distribution")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)
        
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, footer_text)
        self.drawString(54, 35, "Confidential — Presentation Delivery Guide")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 47, 558, 47)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A365D"),
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=14,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#C53030"),
        backColor=colors.HexColor("#EDF2F7"),
        spaceBefore=3,
        spaceAfter=5
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#FFFFFF")
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Jenkins CI/CD Pipeline Presentation Guide", title_style))
    story.append(Paragraph("Student Record Management System — Equal 4-Member Task Distribution & Live Demo Playbook", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=14))

    # Executive Overview
    story.append(Paragraph("Presentation Structure Overview", h1_style))
    overview_p = Paragraph(
        "This project showcases a complete Continuous Integration (CI) pipeline built with Jenkins for a Java Maven application. "
        "The presentation is divided logically into <b>4 equal segments</b> so that every member contributes clearly, "
        "demonstrating architecture, setup, pipeline mechanics, and live automated triggering/failure resilience.",
        body_style
    )
    story.append(overview_p)
    story.append(Spacer(1, 8))

    # Summary Table
    table_data = [
        [
            Paragraph("<b>Member</b>", body_style),
            Paragraph("<b>Presentation Role & Domain</b>", body_style),
            Paragraph("<b>Time Allotted</b>", body_style),
            Paragraph("<b>Core Deliverables</b>", body_style)
        ],
        [
            Paragraph("<b>Member 1</b><br/>(Pranjal)", body_style),
            Paragraph("Introduction, CI/CD Concepts & Architecture", body_style),
            Paragraph("2.5 – 3 mins", body_style),
            Paragraph("Problem statement, CI/CD benefits, architecture flow, prerequisites & Jenkins setup overview.", body_style)
        ],
        [
            Paragraph("<b>Member 2</b><br/>(Khalid)", body_style),
            Paragraph("Jenkins Configuration, Tools & SCM Integration", body_style),
            Paragraph("2.5 – 3 mins", body_style),
            Paragraph("JDK21/Maven3 tool linking, GitHub repository connection, Git plugin setup, initial pipeline job creation.", body_style)
        ],
        [
            Paragraph("<b>Member 3</b><br/>(Keshav)", body_style),
            Paragraph("Pipeline As Code (Jenkinsfile) & Stages", body_style),
            Paragraph("2.5 – 3 mins", body_style),
            Paragraph("Deep dive into Jenkinsfile stages: Checkout, Build, Test, Package, Archive, and JUnit reporting.", body_style)
        ],
        [
            Paragraph("<b>Member 4</b><br/><i>(Presenter 4)</i>", body_style),
            Paragraph("Live Demo: Triggers & Failure Demonstration", body_style),
            Paragraph("3.5 – 4 mins", body_style),
            Paragraph("Live Poll SCM automated build, intentional test failure demo, email alert verification, and restoring green state.", body_style)
        ]
    ]

    t = Table(table_data, colWidths=[80, 160, 75, 189])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # SECTION: DETAILED BREAKDOWN PER MEMBER
    story.append(Paragraph("Detailed Member Breakdown & Speaking Script", h1_style))

    # --- MEMBER 1 ---
    m1_box = [
        Paragraph("<b>Member 1: Pranjal — Project Context & System Architecture</b>", h2_style),
        Paragraph("<b>Goal:</b> Set the stage, explain why CI/CD is needed, and present the high-level architecture.", body_style),
        Paragraph("<b>Key Points to Present:</b>", body_style),
        Paragraph("• <b>What is CI/CD:</b> Explain Continuous Integration as an automated practice where code changes are verified through build and test runs immediately.", bullet_style),
        Paragraph("• <b>Project Overview:</b> Java 21 & Maven project (StudentRecordManagement) designed with unit tests, clean domain separation, and automated packaging.", bullet_style),
        Paragraph("• <b>Environment Stack:</b> Windows 11 host running Jenkins LTS service on port 8080, Git version control, Adoptium Eclipse JDK 21, and Apache Maven 3.9.", bullet_style),
        Paragraph("• <b>Architecture Workflow:</b> Developer pushes to GitHub &rarr; Jenkins detects changes &rarr; Builds & tests code &rarr; Generates artifacts & reports &rarr; Dispatches email alerts.", bullet_style),
        Paragraph("<b>Speaking Tip:</b> Use visual gestures or pointer towards the pipeline flow diagram. Keep the tone confident and introductory.", body_style)
    ]
    story.append(KeepTogether(m1_box))
    story.append(Spacer(1, 8))

    # --- MEMBER 2 ---
    m2_box = [
        Paragraph("<b>Member 2: Khalid — Tool Configuration & SCM Integration</b>", h2_style),
        Paragraph("<b>Goal:</b> Explain how Jenkins connects to external developer tools and GitHub.", body_style),
        Paragraph("<b>Key Points to Present:</b>", body_style),
        Paragraph("• <b>Jenkins Global Tools Setup:</b> Show how <code>Manage Jenkins &rarr; Tools</code> was configured with <code>JDK21</code> and <code>Maven3</code> exact path bindings.", bullet_style),
        Paragraph("• <b>Plugin Ecosystem:</b> Explain key plugins utilized: <i>Pipeline</i>, <i>Git</i>, <i>GitHub</i>, <i>JUnit</i>, <i>Mailer</i>, and <i>Timestamper</i>.", bullet_style),
        Paragraph("• <b>Pipeline Job Configuration:</b> Explain creating the <code>StudentRecord-CI</code> Pipeline job, using 'Pipeline script from SCM', Git repository link, and main branch pointer.", bullet_style),
        Paragraph("• <b>Security & Credentials:</b> Explain how public SCM requires no secrets, but SMTP notification requires secured Google App Passwords.", bullet_style),
        Paragraph("<b>Speaking Tip:</b> Emphasize that automated build execution requires exact naming match between Jenkins Tools and Jenkinsfile declarations.", body_style)
    ]
    story.append(KeepTogether(m2_box))
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # --- MEMBER 3 ---
    m3_box = [
        Paragraph("<b>Member 3: Keshav — Pipeline As Code (Jenkinsfile Anatomy)</b>", h2_style),
        Paragraph("<b>Goal:</b> Explain the declarative pipeline script, stages, and reporting mechanisms.", body_style),
        Paragraph("<b>Key Points to Present:</b>", body_style),
        Paragraph("• <b>Pipeline as Code Paradigm:</b> Explain why storing <code>Jenkinsfile</code> in Git is superior to GUI-only configurations (version controlled, reproducible, audited).", bullet_style),
        Paragraph("• <b>Cross-Platform Runner:</b> Point out the custom Groovy helper function <code>run(cmd)</code> executing <code>bat</code> on Windows or <code>sh</code> on Linux seamlessly.", bullet_style),
        Paragraph("• <b>Stage Breakdown:</b>", body_style),
        Paragraph("&nbsp;&nbsp;1. <b>Checkout:</b> Clones repository from GitHub main branch.", bullet_style),
        Paragraph("&nbsp;&nbsp;2. <b>Build:</b> Executes <code>mvn -B clean compile</code> to compile all Java source files.", bullet_style),
        Paragraph("&nbsp;&nbsp;3. <b>Test:</b> Executes <code>mvn -B test</code> running JUnit 5 test suites.", bullet_style),
        Paragraph("&nbsp;&nbsp;4. <b>Package:</b> Executes <code>mvn -B package</code> to assemble standalone snapshot JAR.", bullet_style),
        Paragraph("&nbsp;&nbsp;5. <b>Archive Artifact:</b> Saves <code>target/*.jar</code> directly onto Jenkins dashboard with fingerprinting.", bullet_style),
        Paragraph("• <b>Post-Execution Actions:</b> Always records test results with <code>junit</code> plugin, prints status, and triggers mail on failure.", bullet_style),
        Paragraph("<b>Speaking Tip:</b> Have the Jenkinsfile on screen or printed so the audience can appreciate the clean declarative structure.", body_style)
    ]
    story.append(KeepTogether(m3_box))
    story.append(Spacer(1, 12))

    # --- MEMBER 4 (EASY, HIGH IMPACT, BULLETPROOF LIVE DEMO) ---
    m4_box = [
        Paragraph("<b>Member 4: Live Automated Trigger & Failure Demonstration</b>", h2_style),
        Paragraph("<b>Goal:</b> Execute the live demonstration smoothly with straightforward, pre-tested commands that never fail.", body_style),
        Paragraph("This role is the most impactful and engaging for the audience, yet simple because the exact commands are scripted step-by-step below.", body_style),
        Spacer(1, 4),
        Paragraph("<b>Live Demo Walkthrough Steps:</b>", h2_style),
        
        Paragraph("<b>Part A: Automated Trigger (Poll SCM Demo)</b>", ParagraphStyle('SubBold', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#2B6CB0"))),
        Paragraph("1. Explain that Jenkins is configured with <code>triggers { pollSCM('H/2 * * * *') }</code>, which checks GitHub every 2 minutes.", bullet_style),
        Paragraph("2. Make a trivial edit to <code>README.md</code> and push from terminal:", bullet_style),
        Paragraph("<code>git commit --allow-empty -m \"docs: test poll scm trigger\"<br/>git push origin main</code>", code_style),
        Paragraph("3. Switch to Jenkins Dashboard and wait 1–2 minutes. Show the audience that a new build starts <i>by itself</i> without clicking any button!", bullet_style),
        Paragraph("4. Open the build console output and highlight line: <code>Started by an SCM change</code>.", bullet_style),
        Spacer(1, 4),

        Paragraph("<b>Part B: Intentional Failure & Alert Demonstration (Requirement 9)</b>", ParagraphStyle('SubBold', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#C53030"))),
        Paragraph("1. Tell the audience: <i>'Now we will prove our CI pipeline protects production by intentionally introducing a bug in our tests.'</i>", bullet_style),
        Paragraph("2. Open <code>src/test/java/com/student/StudentServiceTest.java</code> line 29.", bullet_style),
        Paragraph("3. Change <code>assertEquals(1, service.getAllStudents().size())</code> to <code>assertEquals(99, service.getAllStudents().size())</code>.", bullet_style),
        Paragraph("4. Commit and push the failure:", bullet_style),
        Paragraph("<code>git commit -am \"test: intentional failure demonstration\"<br/>git push origin main</code>", code_style),
        Paragraph("5. Click <b>Build Now</b> (or let Poll SCM trigger). Watch the <b>Test</b> stage fail in bright red!", bullet_style),
        Paragraph("6. Show the <b>Test Result</b> trend (1 failed test) and open the recipient inbox to show the instant automated failure alert email!", bullet_style),
        Spacer(1, 4),

        Paragraph("<b>Part C: Restoring Green State</b>", ParagraphStyle('SubBold', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#276749"))),
        Paragraph("1. Revert line 29 back to <code>1</code> and push:", bullet_style),
        Paragraph("<code>git commit -am \"fix: restore green unit test\"<br/>git push origin main</code>", code_style),
        Paragraph("2. Trigger build and show the pipeline return to 100% blue/green success.", bullet_style)
    ]
    story.append(KeepTogether(m4_box))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # QUICK REFERENCE CHEAT SHEET
    story.append(Paragraph("Live Presentation Quick Reference & Cheat Sheet", h1_style))
    story.append(Paragraph("Keep this cheat sheet handy during the live presentation for immediate troubleshooting and quick answers to examiner questions.", body_style))
    story.append(Spacer(1, 6))

    cheat_data = [
        [
            Paragraph("<b>Question / Situation</b>", body_style),
            Paragraph("<b>Exact Response / Action</b>", body_style)
        ],
        [
            Paragraph("<b>Why use Poll SCM instead of Webhooks?</b>", body_style),
            Paragraph("Localhost Jenkins cannot receive incoming webhooks from public GitHub without a reverse proxy tunnel (e.g. ngrok). Poll SCM provides automated periodic polling without requiring public ingress.", body_style)
        ],
        [
            Paragraph("<b>Why did we use App Password for Gmail?</b>", body_style),
            Paragraph("Google disabled basic authentication for security. Jenkins SMTP relies on a dedicated 16-character App Password generated under Google Account 2-Step Verification.", body_style)
        ],
        [
            Paragraph("<b>What happens if a stage fails?</b>", body_style),
            Paragraph("Downstream stages (like Package and Archive) are automatically skipped. The <code>post { always { ... } }</code> block still publishes the JUnit test failure report, and <code>post { failure { ... } }</code> sends an email notification.", body_style)
        ],
        [
            Paragraph("<b>How does cross-platform support work?</b>", body_style),
            Paragraph("The Jenkinsfile defines a helper <code>run(cmd)</code> using <code>isUnix()</code> check to execute <code>bat</code> commands on Windows and <code>sh</code> on Linux/Ubuntu.", body_style)
        ]
    ]

    ct = Table(cheat_data, colWidths=[170, 334])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(ct)
    story.append(Spacer(1, 14))

    # Live Demo Terminal One-Liners Box
    terminal_box = [
        Paragraph("<b>Copy-Paste Terminal Commands for Live Demo:</b>", h2_style),
        Paragraph("<code># 1. Trigger Poll SCM automatically:</code>", body_style),
        Paragraph("<code>git commit --allow-empty -m \"docs: test poll scm\" && git push origin main</code>", code_style),
        Spacer(1, 2),
        Paragraph("<code># 2. After editing StudentServiceTest.java to introduce failure:</code>", body_style),
        Paragraph("<code>git commit -am \"test: deliberate failure for demo\" && git push origin main</code>", code_style),
        Spacer(1, 2),
        Paragraph("<code># 3. After reverting StudentServiceTest.java back to normal:</code>", body_style),
        Paragraph("<code>git commit -am \"fix: restore passing tests\" && git push origin main</code>", code_style),
    ]
    story.append(KeepTogether(terminal_box))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF successfully: {filename}")

if __name__ == '__main__':
    pdf_path = os.path.join(r"d:\Student", "Jenkins_Presentation_Guide_4_Members.pdf")
    build_pdf(pdf_path)
