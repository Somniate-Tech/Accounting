from sqlalchemy.orm import Session

from app.modules.subscriptions.subscription_payments.model import (
    SubscriptionPayment
)


def create_subscription_payment_repo(
    db: Session,
    payment: SubscriptionPayment
):
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


def get_subscription_payment_by_id_repo(
    db: Session,
    payment_id: int
):
    return (
        db.query(SubscriptionPayment)
        .filter(
            SubscriptionPayment.id == payment_id
        )
        .first()
    )


def get_subscription_payments_repo(
    db: Session,
    organization_id: int
):
    return (
        db.query(SubscriptionPayment)
        .filter(
            SubscriptionPayment.organization_id
            == organization_id
        )
        .order_by(
            SubscriptionPayment.id.desc()
        )
        .all()
    )


def update_subscription_payment_repo(
    db: Session,
    payment: SubscriptionPayment
):
    db.commit()
    db.refresh(payment)

    return payment