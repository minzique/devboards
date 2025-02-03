from sqlalchemy.orm import Session
from src.models.db.company import CompanyModel

def seed_companies(db: Session):
    companies = [
        {
            "name": "Zebra",
            "slug": "zebra",
            "logo_url": "/zebra-logo.png",
            "website": "https://zebra.com"
        },
        {
            "name": "Rootcode",
            "slug": "rootcode", 
            "logo_url": "https://rootcode.io/images/rootcode-logo.png",
            "website": "https://rootcode.io"
        },
        {
            "name": "WSO2",
            "slug": "wso2",
            "logo_url": "/wso2-logo.png",
            "website": "https://wso2.com"
        },
        
        {
            "name": "Google",
            "slug": "google",
            "logo_url": "/google-logo.png",
            "website": "https://google.com"  
        }
    ]
    
    for company_data in companies:
        company = db.query(CompanyModel).filter_by(slug=company_data["slug"]).first()
        if not company:
            company = CompanyModel(**company_data)
            db.add(company)
    
    db.commit()
