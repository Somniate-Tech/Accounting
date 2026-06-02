from sqlalchemy.orm import Session

from app.modules.admin.repository import (
    AdminRepository
)
from fastapi import HTTPException

class AdminService:

    @staticmethod
    def get_dashboard(
        db: Session
    ):

        return (
            AdminRepository.get_dashboard_stats(
                db=db
            )
        )
    
    @staticmethod
    def get_all_organizations(
        db: Session
    ):

        return (
            AdminRepository.get_all_organizations(
                db=db
            )
        )
    
    @staticmethod
    def get_all_users(
        db: Session
    ):

        return (
            AdminRepository.get_all_users(
                db=db
            )
        )
    
    @staticmethod
    def get_all_subscriptions(
        db: Session
    ):

        return (
            AdminRepository.get_all_subscriptions(
                db=db
            )
        )
    
    @staticmethod
    def deactivate_organization(
        db: Session,
        organization_id: int
    ):

        organization = (
            AdminRepository.get_organization_by_id(
                db=db,
                organization_id=organization_id
            )
        )

        if not organization:

            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        organization.is_active = False

        db.commit()

        db.refresh(organization)

        return {
            "message":
            "Organization deactivated successfully"
        }
    

    @staticmethod
    def activate_organization(
        db: Session,
        organization_id: int
    ):

        organization = (
            AdminRepository.get_organization_by_id(
                db=db,
                organization_id=organization_id
            )
        )

        if not organization:

            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        organization.is_active = True

        db.commit()

        db.refresh(organization)

        return {
            "message":
            "Organization activated successfully"
        }
    
    @staticmethod
    def get_expired_subscriptions(
        db: Session
    ):

        return (
            AdminRepository.get_expired_subscriptions(
                db=db
            )
        )


    @staticmethod
    def get_trial_subscriptions(
        db: Session
    ):

        return (
            AdminRepository.get_trial_subscriptions(
                db=db
            )
        )


    @staticmethod
    def get_expiring_subscriptions(
        db: Session
    ):

        return (
            AdminRepository.get_expiring_subscriptions(
                db=db
            )
        )
    
    @staticmethod
    def get_revenue_dashboard(
        db: Session
    ):

        return (
            AdminRepository.get_revenue_dashboard(
                db=db
            )
        )