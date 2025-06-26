from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.utils.crypto import get_random_string
import datetime
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm, LoginForm  # ✅ LoginForm needed
from django.contrib.auth.hashers import check_password  # ✅ for secure password check
from .forms import PasswordConfirmForm,TransferForm,DepositForm
from .forms import WithdrawForm  
from .models import PersonalDetails, Account, Transaction
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)

            # In future: hash password here
            user.password = make_password(form.cleaned_data['password'])
            user.created_at = datetime.datetime.now()
            user.save()

            # Generate random account number
            acc_no = get_random_string(length=10, allowed_chars='0123456789')

            Account.objects.create(
                personal=user,
                account_number=acc_no,
                balance=0.00
            )

            return render(request, 'registration_success.html', {'acc_no': acc_no})
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            acc_no = form.cleaned_data['account_number']
            password = form.cleaned_data['password']

            try:
                account = Account.objects.get(account_number=acc_no)
                user = account.personal
                if check_password(password, user.password):
                    # Save session (optional)
                    request.session['user_id'] = user.id
                    request.session['account_id'] = account.id
                    return redirect('dashboard')  # you can create dashboard view later
                else:
                    error = "Invalid password"
            except Account.DoesNotExist:
                error = "Account not found"
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})



def withdraw(request):
    if 'user_id' not in request.session:
        return redirect('login')

    # ✅ Allow POST to proceed if user just confirmed
    if request.method == 'GET':
        if request.session.get('authenticated_action') != 'withdraw':
            return redirect('/confirm-password/?next_action=withdraw')
        request.session['authenticated_action'] = None  # clear only once

    user = PersonalDetails.objects.get(id=request.session['user_id'])
    account = Account.objects.get(personal=user)
    message = ""

    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                message = "❌ Insufficient balance."
            else:
                account.balance -= amount
                account.save()
                Transaction.objects.create(
                    sender_account=account,
                    receiver_account=None,
                    amount=amount,
                    transaction_type='withdraw'
                )
                message = "✅ Withdrawal successful."
    else:
        form = WithdrawForm()

    return render(request, 'bank_app/withdraw.html', {'form': form, 'message': message})

def transfer(request):
    if 'user_id' not in request.session:
        return redirect('login')

    # ✅ Allow GET access only if password confirmed
    if request.method == 'GET':
        if request.session.get('authenticated_action') != 'transfer':
            return redirect('/confirm-password/?next_action=transfer')
        request.session['authenticated_action'] = None  # clear session only once

    user = PersonalDetails.objects.get(id=request.session['user_id'])
    sender_account = Account.objects.get(personal=user)
    message = ""
    transaction_id = None

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            receiver_acc = form.cleaned_data['receiver_account']
            amount = form.cleaned_data['amount']

            try:
                receiver_account = Account.objects.get(account_number=receiver_acc)
                if receiver_account == sender_account:
                    message = "❌ Cannot transfer to your own account."
                elif sender_account.balance < amount:
                    message = "❌ Insufficient balance."
                else:
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()

                    transaction = Transaction.objects.create(
                        sender_account=sender_account,
                        receiver_account=receiver_account,
                        amount=amount,
                        transaction_type='transfer'
                    )

                    transaction_id = transaction.id
                    message = f"✅ Transfer successful. Transaction ID: {transaction_id}"

            except Account.DoesNotExist:
                message = "❌ Receiver account does not exist."
    else:
        form = TransferForm()

    return render(request, 'bank_app/transfer.html', {
        'form': form,
        'message': message,
        'tr_id': transaction_id
    })


def confirm_password(request):
    next_action = request.GET.get('next_action')
    account_id = request.session.get('account_id')
    if not account_id:
        return redirect('login')

    if request.method == 'POST':
        form = PasswordConfirmForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            account = Account.objects.get(id=account_id)
            if check_password(password, account.personal.password):
                request.session['authenticated_action'] = next_action
                return redirect(next_action)  # e.g. /withdraw/
            else:
                form.add_error('password', 'Incorrect password')
    else:
        form = PasswordConfirmForm()

    return render(request, 'confirm_password.html', {'form': form, 'next': next_action})

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = PersonalDetails.objects.get(id=request.session['user_id'])
    account = Account.objects.get(personal=user)

    context = {
        'name': user.full_name,
        'account_number': account.account_number,
        'balance': account.balance
    }
    return render(request, 'bank_app/dashboard.html', context)

def deposit(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = PersonalDetails.objects.get(id=request.session['user_id'])
    account = Account.objects.get(personal=user)
    message = ""

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()

            Transaction.objects.create(
                sender_account=account,
                receiver_account=None,
                amount=amount,
                transaction_type='deposit'
            )
            message = "✅ Deposit successful!"
    else:
        form = DepositForm()

    return render(request, 'bank_app/deposit.html', {'form': form, 'message': message})

def transaction_history(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = PersonalDetails.objects.get(id=request.session['user_id'])
    account = Account.objects.get(personal=user)

    transactions = Transaction.objects.filter(
        sender_account=account
    ) | Transaction.objects.filter(
        receiver_account=account
    )
    transactions = transactions.order_by('-timestamp')

    return render(request, 'bank_app/transaction_history.html', {
        'transactions': transactions,
        'account': account  # ✅ required
    })

def home(request):
    return render(request, 'home.html')

def logout(request):
    request.session.flush()  # ✅ clears all session data
    return redirect('home')  # or use 'login' if preferred

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin123':  # 👈 Simple check
            request.session['is_admin'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'admin/admin_login.html')

from .models import PersonalDetails, Account, Transaction

def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    users = Account.objects.select_related('personal').all()
    return render(request, 'admin/admin_dashboard.html', {'users': users})

def admin_transactions(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    transactions = Transaction.objects.select_related('sender_account', 'receiver_account').order_by('-timestamp')
    return render(request, 'admin/admin_transaction.html', {'transactions': transactions})


