from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from models.image import Image
from instagram_web.util.braintree import gateway
from models.donation import Donation

donations_blueprint = Blueprint(
    'donations', __name__, template_folder="templates")


@donations_blueprint.route('/<image_id>/new', methods=["GET"])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash("No image found with ID provided")
        return redirect(url_for('users.show'))

    client_token = gateway.client_token.generate()

    if not client_token:
        flash("unable to obtain token boo")
        return redirect(url_for('users.show'))

    return render_template('donations/new.html', image=image, client_token=client_token)


@donations_blueprint.route('/<image_id>/', methods=["POST"])
@login_required
def create(image_id):
    nonce = request.form.get('payment_method_nonce')

    if not nonce:
        flash("invalid cred card deets")
        return redirect(url_for('users.index'))

    image = Image.get_or_none(Image.id == image_id)

    # image could have been deleted, so double check first
    if not image:
        flash("no image found with ID provided")
        return redirect(url_for('users.index'))

    amount = request.form.get('amount')

    if not amount:
        flash("no amount provided")
        return redirect(url_for('users.index'))

    # make sure sale goes through
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    # amounts more than 1000 WONT BE ACCEPTED
    # can check result
    # result.is_success
    # should return True

    if not result.is_success:
        flash("unable to complete transaction")
        return redirect(request.referrer)
        # redirect to where they came from

    donation = Donation(amount=amount, image_id=image.id,
                        user_id=current_user.id)

    if not donation.save():
        flash('donation successful but error creating record')
        return redirect(url_for('users.index'))

    flash(f"successfully donated RM{amount} thankiu C:")
    return redirect(url_for('users.index'))
