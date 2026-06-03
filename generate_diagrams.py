import urllib.request
import os

diagrams = {
    "packages_fonctionnels.png": """@startuml
skinparam shadowing false
skinparam packageStyle rectangle
skinparam defaultFontSize 12
skinparam packageFontSize 13
skinparam packageBorderThickness 1.5
skinparam backgroundColor white
skinparam arrowColor #555555

package "Gestion des Utilisateurs & Profils" as auth #E2EFDA {
}

package "Gestion Commerciale (CRM)" as crm #DAE8FC {
}

package "Productivité & Support" as prod #FFF2CC {
}

package "Communication & Messagerie" as comm #FFE6CC {
}

package "Importation & Exportation" as import #F5F5F5 {
}

package "Intelligence Artificielle" as ia #FCE4EC {
}

package "Analytics & Reporting" as analytics #DAEEF3 {
}

crm ..> auth : <<use>>
prod ..> auth : <<use>>
comm ..> auth : <<use>>

import ..> crm : <<use>>
ia ..> crm : <<use>>
analytics ..> crm : <<use>>
analytics ..> prod : <<use>>

@enduml""",

    "diagramme_classes_enumerations.png": """@startuml
skinparam shadowing false
skinparam classAttributeIconSize 0
skinparam defaultFontSize 11
skinparam packageStyle rectangle
skinparam backgroundColor white
skinparam arrowColor #555555
skinparam classBorderColor #444444
skinparam classHeaderBackgroundColor #E2EFDA

package "Enumerations" as enums <<Rectangle>> {
  enum Role {
    ADMIN
    MANAGER
    SALES_REP
  }
  enum CompanyIndustry {
    TECHNOLOGY
    FINANCE
    HEALTHCARE
    RETAIL
    OTHER
  }
  enum CompanySize {
    STARTUP
    SMALL
    MEDIUM
    LARGE
    ENTERPRISE
  }
  enum ContactStatus {
    ACTIVE
    INACTIVE
  }
  enum LeadStatus {
    NEW
    CONTACTED
    QUALIFIED
    UNQUALIFIED
  }
  enum DealStatus {
    OPEN
    WON
    LOST
  }
  enum ImportStatus {
    PENDING
    COMPLETED
    FAILED
  }
  enum Priority {
    LOW
    MEDIUM
    HIGH
    URGENT
  }
  enum TaskStatus {
    TODO
    IN_PROGRESS
    DONE
  }
  enum TicketStatus {
    OPEN
    IN_PROGRESS
    RESOLVED
    CLOSED
  }
  enum PipelineStage {
    PROSPECTING
    QUALIFICATION
    PROPOSAL
    NEGOTIATION
    CLOSED
  }
  
  Role -[hidden]right-> CompanyIndustry
  CompanyIndustry -[hidden]right-> CompanySize
  CompanySize -[hidden]right-> ContactStatus
  
  LeadStatus -[hidden]right-> DealStatus
  DealStatus -[hidden]right-> ImportStatus
  ImportStatus -[hidden]right-> Priority
  
  TaskStatus -[hidden]right-> TicketStatus
  TicketStatus -[hidden]right-> PipelineStage
  
  Role -[hidden]down-> LeadStatus
  LeadStatus -[hidden]down-> TaskStatus
}
@enduml""",

    "diagramme_classes_entites.png": """@startuml
skinparam shadowing false
skinparam classAttributeIconSize 0
skinparam defaultFontSize 11
skinparam packageStyle rectangle
skinparam backgroundColor white
skinparam arrowColor #555555
skinparam classBorderColor #444444
skinparam classHeaderBackgroundColor #E2EFDA

' ==========================================
' COLUMN 1: CRM & SALES (Left)
' ==========================================
class Company {
  id : Int
  name : String
  companyIndustry : CompanyIndustry
  companySize : CompanySize
  location : String
  revenue : Float
}

class Contact {
  id : Int
  name : String
  email : String
  phone : String
  status : ContactStatus
}

class LeadContact {
  id : Int
  role : String
}

class Lead {
  id : Int
  name : String
  email : String
  phone : String
  status : LeadStatus
  probability : Float
  dealValue : Float
}

class LeadScore {
  id : Int
  score : Float
  probability : Float
  temperature : String
}

class Deal {
  id : Int
  name : String
  amount : Float
  probability : Float
  status : DealStatus
}

' Enforce Column 1 vertical alignment
Company -[hidden]down-> Contact
Contact -[hidden]down-> LeadContact
LeadContact -[hidden]down-> Lead
Lead -[hidden]down-> LeadScore
LeadScore -[hidden]down-> Deal

' ==========================================
' COLUMN 2: USER & UTILITIES (Middle)
' ==========================================
class User {
  id : Int
  name : String
  email : String
  role : Role
}

class Activity {
  id : Int
  type : String
  title : String
  description : String
  entity : String
}

class CsvImport {
  id : Int
  fileName : String
  status : ImportStatus
  numberOfRows : Int
}

class Notification {
  id : Int
  type : String
  message : String
  isRead : Boolean
  degree : Priority
}

class Task {
  id : Int
  title : String
  dueDate : DateTime
  status : TaskStatus
  priority : Priority
}

class Note {
  id : Int
  content : String
}

' Enforce Column 2 vertical alignment
User -[hidden]down-> Activity
Activity -[hidden]down-> CsvImport
CsvImport -[hidden]down-> Notification
Notification -[hidden]down-> Task
Task -[hidden]down-> Note

' ==========================================
' COLUMN 3: PROCESS & COMMS (Right)
' ==========================================
class Ticket {
  id : Int
  title : String
  description : String
  status : TicketStatus
  priority : Priority
}

class Email {
  id : Int
  from : String
  to : String
  subject : String
  status : String
}

class Pipeline {
  id : Int
  name : String
  stage : PipelineStage
}

class PipelineDate {
  order : Int
}

class Date {
  id : Int
  date : DateTime
}

class Chat {
  id : String
  name : String
  isGroup : Boolean
}

class Message {
  id : String
  content : String
  isRead : Boolean
}

' Enforce Column 3 vertical alignment
Ticket -[hidden]down-> Email
Email -[hidden]down-> Pipeline
Pipeline -[hidden]down-> PipelineDate
PipelineDate -[hidden]down-> Date
Date -[hidden]down-> Chat
Chat -[hidden]down-> Message

' Enforce horizontal separation of columns
Company -[hidden]right-> User
User -[hidden]right-> Ticket

' ==========================================
' RELATIONS
' ==========================================
User "1" -up-> "*" User : manages >
User "1" -left-> "*" Company : manages >
User "1" --> "*" Contact : contacts >
User "1" --> "*" Deal : negotiates >
User "1" --> "*" Pipeline : owns >

User "1" -down-> "*" Activity : performs >
User "1" -down-> "*" CsvImport : imports >
User "1" -down-> "*" Notification : receives >
User "1" -down-> "*" Task : creates >
User "1" -down-> "*" Note : writes >

Company "1" --> "*" Contact : employs >
Company "1" --> "*" Lead : generates >

Contact "1" --> "*" LeadContact : linked via >
Lead "1" --> "*" LeadContact : includes >

Lead "1" --> "0..1" LeadScore : obtains >
Lead "1" --> "*" Deal : converts to >
Lead "1" --> "*" Task : concerns >
Lead "1" --> "*" Ticket : raises >
Lead "1" --> "*" Note : has >
Lead "1" --> "*" Email : receives >

Contact "1" --> "*" Ticket : opens >
Contact "1" --> "*" Email : exchanges >

Pipeline "1" --> "*" Lead : contains >
Pipeline "1" --> "*" Deal : tracks >
Pipeline "1" --> "*" PipelineDate : structured by >
PipelineDate "*" --> "1" Date : references >

User "1" --> "*" Message : sends >
Chat "1" --> "*" Message : contains >
User "*" -right-> "*" Chat : participates in >
@enduml""",

    "dsc_authentification.png": """@startuml
actor Utilisateur
participant "AuthController" as ctrl
participant "AuthService" as auth
participant "UsersService" as users
database "MySQL (Prisma)" as db

Utilisateur -> ctrl : POST /auth/login (email, password)
activate ctrl
ctrl -> auth : validateUser(email, password)
activate auth
auth -> users : findByEmail(email)
activate users
users -> db : SELECT * FROM User WHERE email = ?
activate db
db --> users : User Entity
deactivate db
users --> auth : User
deactivate users
auth -> auth : bcrypt.compare(password, hash)
auth --> ctrl : User Validated
deactivate auth

ctrl -> auth : login(User)
activate auth
auth -> auth : sign(JWT Payload)
auth --> ctrl : { access_token }
deactivate auth
ctrl --> Utilisateur : 200 OK { access_token }
deactivate ctrl
@enduml""",

    "dsc_scoring_ia.png": """@startuml
actor Utilisateur
participant "LeadsController" as ctrl
participant "LeadsService" as srv
participant "PrismaClient" as db
participant "FastAPI AI Agent" as ia

Utilisateur -> ctrl : POST /leads/:id/score
activate ctrl
ctrl -> srv : calculateScore(id)
activate srv
srv -> db : findUnique(Lead, Contact, Company)
activate db
db --> srv : Lead Data
deactivate db

srv -> ia : POST /predict (Lead Data)
activate ia
ia -> ia : ML Model Inference
ia --> srv : 200 OK { score: 85 }
deactivate ia

srv -> db : update(Lead, { aiScore: 85 })
activate db
db --> srv : Updated Lead
deactivate db

srv --> ctrl : Updated Lead
deactivate srv
ctrl --> Utilisateur : 200 OK (Lead with Score)
deactivate ctrl
@enduml""",

    "dsc_gemini_email.png": """@startuml
actor "Sales Rep" as user
participant "AiEmailModal\\n(Next.js)" as front
participant "AiController\\n(NestJS)" as ctrl
participant "AiService" as srv
participant "Google Gemini API" as gemini

user -> front : Clic "Générer Email"
activate front
front -> ctrl : POST /ai/generate-email (leadId)
activate ctrl
ctrl -> srv : generateEmailForLead(leadId)
activate srv
srv -> srv : gatherContext(Lead, Company)
srv -> gemini : POST /v1/models/gemini-pro:generateContent
activate gemini
note right: Prompt: "Génère un email d'approche pour..."
gemini --> srv : Generated Text
deactivate gemini
srv --> ctrl : { content: "..." }
deactivate srv
front <-- ctrl : 200 OK { content }
deactivate ctrl
front --> user : Affiche l'email généré (éditable)
deactivate front
@enduml""",

    "dcp_gerer_leads.png": """@startuml
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam shadowing false

' --- Top Tier: Dialogue (Boundary) ---
class "LeadsTable" as ui <<Boundary>> {
  + displayLeads()
  + handleSort()
  + handleFilter()
}

class "LeadDetailsModal" as modal <<Boundary>> {
  + showDetails(lead)
  + updateStatus()
}

' --- Middle Tier: Controle (Control) ---
class "LeadsController" as ctrl <<Control>> {
  + getLeads()
  + getLeadById()
  + updateLead()
}

class "LeadsService" as srv <<Control>> {
  + findAll()
  + findOne(id)
  + update(id, dto)
}

' --- Bottom Tier: Entite (Entity) ---
class "Lead" as lead <<Entity>> {
  + id: Int
  + status: String
  + aiScore: Float
}

class "Contact" as contact <<Entity>> {
  + id: Int
  + email: String
}

class "Company" as company <<Entity>> {
  + id: Int
  + name: String
}

' --- Layout Structure (3 Tiers) ---
ui -[hidden]right-> modal
ctrl -[hidden]right-> srv
lead -[hidden]right-> contact
contact -[hidden]right-> company

ui -[hidden]down-> ctrl
modal -[hidden]down-> ctrl
ctrl -[hidden]down-> lead
srv -[hidden]down-> lead

' --- Connections ---
ui ..> ctrl : HTTP GET
modal ..> ctrl : HTTP GET/PATCH
ctrl --> srv : invokes
srv --> lead : manages
srv --> contact : manages
srv --> company : manages
lead "1" -- "1" contact : belongs to >
lead "1" -- "1" company : belongs to >
@enduml""",

    "dcp_import_csv.png": """@startuml
skinparam style strictuml
skinparam classAttributeIconSize 0
skinparam shadowing false

' --- DIALOGUE (Boundary) ---
class "CSVImportWizard" as wizard <<Boundary>> {
  + uploadFile(file)
  + mapColumns()
  + confirmImport()
}

' --- CONTROLE (Control) ---
class "ImportController" as ctrl <<Control>> {
  + uploadCsv()
  + processImport()
}

class "ImportService" as srv <<Control>> {
  + parseCsv(buffer)
  + validateRows()
  + bulkInsert()
}

' --- ENTITE / DTO ---
class "CreateLeadDto" as dto <<DTO>> {
  + firstName: String
  + lastName: String
  + email: String
  + companyName: String
}

class "Lead" as lead <<Entity>> {
  + id: Int
  + status: String
}

class "Contact" as contact <<Entity>> {
  + id: Int
  + email: String
}

' --- VERTICAL LAYOUT FOR COLUMNS ---
ctrl -[hidden]down-> srv
dto -[hidden]down-> lead
lead -[hidden]down-> contact

' --- HORIZONTAL COLUMN LINKING ---
wizard -[hidden]right-> ctrl
ctrl -[hidden]right-> dto

' --- CONNECTIONS ---
wizard ..> ctrl : HTTP POST (multipart/form-data)
ctrl --> srv : delegates
srv ..> dto : validates via class-validator
srv --> lead : creates (Prisma)
srv --> contact : creates (Prisma)
@enduml""",

    "diagramme_composants_frontend.png": """@startuml
skinparam style strictuml
skinparam shadowing false
skinparam defaultFontSize 13
skinparam componentStyle rectangle
skinparam backgroundColor white
skinparam arrowColor #555555

package "Application Front-End (Next.js / React)" {
  [Pages d'Interface\\n(Auth, CRM, Chat, CSV)] as ui <<Interface UI>> #E2EFDA
  [Gestion d'État\\n(Zustand Stores)] as state <<State Store>> #DAE8FC
  [Client de Communication\\n(Axios & Socket.io)] as client <<API Client>> #FFF2CC
}

package "Back-End & Services" {
  [API Applicative\\n(NestJS Backend)] as backend <<API REST>> #FFE6CC
}

' Relations simples et claires
ui --> state : Lit / Met à jour l'état
ui --> client : Initie les requêtes
client --> backend : Appels HTTP & Événements WS
@enduml""",

    "architecture_backend.png": """@startuml
skinparam style strictuml
skinparam shadowing false
skinparam defaultFontSize 12
skinparam packageStyle rectangle
skinparam backgroundColor white
skinparam arrowColor #555555

package "Module Principal (AppModule)" as app #E2EFDA {
}

package "Authentification (AuthModule)" as auth #DAE8FC {
  [AuthController] as auth_ctrl
  [AuthService] as auth_srv
}

package "Gestion des Leads (LeadsModule)" as leads #FFF2CC {
  [LeadsController] as leads_ctrl
  [LeadsService] as leads_srv
}

package "Intelligence Artificielle (AiModule)" as ai #FCE4EC {
  [AiController] as ai_ctrl
  [AiService] as ai_srv
}

package "Base de Données (PrismaModule)" as prisma #F5F5F5 {
  [PrismaService] as prisma_srv
}

' Relations d'importation de modules
app --> auth : imports
app --> leads : imports
app --> ai : imports
app --> prisma : imports

' Relations internes et externes
auth_ctrl --> auth_srv : utilise
auth_srv --> prisma_srv : interroge DB

leads_ctrl --> leads_srv : utilise
leads_srv --> prisma_srv : interroge DB

ai_ctrl --> ai_srv : utilise
ai_srv --> prisma_srv : interroge DB
@enduml""",

    "architecture_microservices.png": """@startuml
skinparam style strictuml
skinparam shadowing false
skinparam defaultFontSize 12
skinparam componentStyle rectangle
skinparam backgroundColor white
skinparam arrowColor #555555

node "Client / Frontend" as client_tier {
  [Next.js Application] as nextjs #E2EFDA
}

node "Backend Applicatif" as backend_tier {
  [NestJS Server] as nestjs #DAE8FC
  database "MySQL Database" as mysql #F5F5F5
}

node "Microservice IA" as ai_tier {
  [FastAPI Service (Python)] as fastapi #FFF2CC
  [Random Forest Model] as rf_model #FFF2CC
}

node "Services Cloud Externes" as ext_tier {
  [API Google Gemini] as gemini #FFE6CC
}

' Flux de données
nextjs --> nestjs : 1. Requêtes REST (HTTP) / WebSockets
nestjs --> mysql : 2. Persistance (Prisma ORM)

nestjs -right-> fastapi : 3. Calcul Score IA (POST /predict)
fastapi --> rf_model : 4. Modèle d'inférence

nestjs --> gemini : 5. RAG Chatbot & Génération d'Emails
@enduml""",

    "diagramme_deploiement.png": """@startuml
skinparam style strictuml
skinparam shadowing false
skinparam defaultFontSize 11
skinparam componentStyle rectangle
skinparam backgroundColor white
skinparam arrowColor #555555

' Nodes & Devices
node "Poste Client" as client_node #E2EFDA {
  [Navigateur Web] as browser <<Component>>
}

node "Cluster Kubernetes (K8s)" as cluster #F2F4F7 {
  
  node "Pod Frontend" as front_node #DAE8FC {
    [Next.js Server] as nextjs <<Component>>
    [Routing Middleware] as middleware <<Component>>
  }
  
  node "Pod Backend" as back_node #FFF2CC {
    [NestJS API Server] as nestjs <<Component>>
    [Socket.io Gateway] as ws <<Component>>
    [Prisma Client] as prisma <<Component>>
  }
  
  node "Pod Service IA" as ai_node #FCE4EC {
    [FastAPI Server] as fastapi <<Component>>
    [Random Forest Model] as rf_model <<Component>>
  }
  
  node "Pod Database" as db_node #F5F5F5 {
    database "MySQL 8" as mysql <<Database>>
  }
}

node "DevOps & CI/CD Pipeline" as devops #E8F5E9 {
  [GitHub Actions] as github <<Tool>>
  [Docker Hub Registry] as dockerhub <<Registry>>
  [Helm Charts] as helm <<Tool>>
}

node "Services Externes" as ext_services #E1F5FE {
  [API Google Gemini] as gemini <<Service>>
  [Serveur Mailtrap] as mailtrap <<Service>>
}

node "Décisionnel" as bi_node #FFF9C4 {
  [Power BI Desktop] as powerbi <<Application>>
}

' Links & Communication Protocols
browser -down-> nextjs : HTTPS (Port 3001)
nextjs -down-> nestjs : HTTP REST (Port 3000)
nextjs -down-> ws : WebSockets (Socket.io)

nestjs -right-> fastapi : HTTP POST /predict (Port 8000)
fastapi -down-> rf_model : charge & exécute
nestjs -down-> mysql : TCP (Port 3006 via Prisma)

nestjs -right-> gemini : HTTPS (API Key)
nestjs -down-> mailtrap : SMTP (Port 2525)
powerbi -down-> mysql : ODBC/MySQL Connexion

github -right-> dockerhub : Push Docker Images
dockerhub -down-> cluster : Pull Images
helm -down-> cluster : Déploiement K8s
@enduml""",

    "diagramme_blocs_internes.png": """@startuml
skinparam shadowing false
skinparam classAttributeIconSize 0
skinparam defaultFontSize 11
skinparam packageStyle rectangle
skinparam backgroundColor #EEEEEE

package "Frameworks" as fw {
  class "Controller" as ctrl_base {
    + execute(req: Request): Response
  }
  class "Component" as comp_base {
  }
  ctrl_base ..> comp_base
}

package "Logique applicative" as log_app {
  class "<<Controller>>\\nLeadsController" as ctrl1 #F2B8B5 {
    + execute() : void
  }
  
  class "<<Controller>>\\nImportController" as ctrl2 #B4C7E7 {
    + execute() : void
  }
  
  class "<<Service>>\\nLeadsService" as srv #EAEAEA {
    + validerLead()
    + recupererLeadsList()
  }
  
  class "<<Store>>\\nLeadsStore" as store #EAEAEA {
    <<liste>> leadsDisponibles: Lead[*]
    leadChoisi: Lead
    --
    + validerLead()
    + recupererLeadsList()
    + ajouterLeadChoisi()
  }
  
  srv <|-- store
}

package "Logique métier" as log_metier {
  class "Lead" as ent1 #F2B8B5 {
    + assignerContact()
    + rechargerScore()
    + getCurrentLead()
  }
  
  class "Contact" as ent2 #B4C7E7 {
    + getContactById()
    + renewContact()
  }
  
  class "Company" as ent3 #B4C7E7 {
    - dateCreation: Date
    - status: boolean
    - revenusGeneres: double
  }
  
  ent1 "0..*" -right- "0..*" ent3
  ent1 "1" -right- "0..*" ent2
}

package "Présentation" as presentation {
  class "<<Component>>\\nLeadDetailsModal" as comp1 #EAEAEA {
    + validerLead()
    + consulterProfil()
    + annuler()
  }
  
  class "<<Component>>\\nLeadsTable" as comp2 #EAEAEA {
    + recupererLeadsListe()
    + choisirUnLead()
    + rechargerScore()
    + consulterProfil()
  }
  
  comp1 <.. comp2 : <<link>>
}

ctrl_base <|-- ctrl1
ctrl_base <|-- ctrl2

comp_base <|-- comp1

ctrl1 -down-> "1" ent1
ctrl2 -down-> "1" ent2

store <-- comp1

@enduml"""
}

images_dir = r"c:\Users\ASUS\Desktop\projet-pfe\rapport\images"
os.makedirs(images_dir, exist_ok=True)

for filename, puml_content in diagrams.items():
    print(f"Generating {filename}...")
    req = urllib.request.Request("https://kroki.io/plantuml/png", data=puml_content.encode('utf-8'))
    req.add_header('Content-Type', 'text/plain')
    req.add_header('User-Agent', 'Mozilla/5.0')
    try:
        with urllib.request.urlopen(req) as response:
            with open(os.path.join(images_dir, filename), 'wb') as f:
                f.write(response.read())
        print(f"Saved {filename}")
    except Exception as e:
        print(f"Failed {filename}: {e}")
