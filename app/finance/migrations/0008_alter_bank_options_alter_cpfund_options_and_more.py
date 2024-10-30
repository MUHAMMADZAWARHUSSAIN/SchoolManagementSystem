# Generated by Django 4.2.16 on 2024-10-30 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0009_merge_20241028_1732'),
        ('finance', '0007_cpfund_created_by_cpfund_employee_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bank',
            options={'verbose_name': 'Bank', 'verbose_name_plural': 'Banks'},
        ),
        migrations.AlterModelOptions(
            name='cpfund',
            options={'verbose_name': 'CP Fund', 'verbose_name_plural': 'CP Funds'},
        ),
        migrations.AlterModelOptions(
            name='cpfunddeposits',
            options={'verbose_name': 'CP Fund Deposit', 'verbose_name_plural': 'CP Fund Deposits'},
        ),
        migrations.AlterModelOptions(
            name='employeearrears',
            options={'verbose_name': 'Employee Arrears', 'verbose_name_plural': 'Employee Arrears'},
        ),
        migrations.AlterModelOptions(
            name='eobipaid',
            options={'verbose_name': 'EOBI Payment', 'verbose_name_plural': 'EOBI Payments'},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name': 'Expense', 'verbose_name_plural': 'Expenses'},
        ),
        migrations.AlterModelOptions(
            name='incometaxrates',
            options={'verbose_name': 'Income Tax Rate', 'verbose_name_plural': 'Income Tax Rates'},
        ),
        migrations.AlterModelOptions(
            name='incometaxsession',
            options={'verbose_name': 'Income Tax Session', 'verbose_name_plural': 'Income Tax Sessions'},
        ),
        migrations.AlterModelOptions(
            name='installmentpaid',
            options={'verbose_name': 'Installment Paid', 'verbose_name_plural': 'Installments Paid'},
        ),
        migrations.AlterModelOptions(
            name='loan',
            options={'verbose_name': 'Loan', 'verbose_name_plural': 'Loans'},
        ),
        migrations.AlterModelOptions(
            name='monthclosing',
            options={'verbose_name': 'Month Closing', 'verbose_name_plural': 'Month Closings'},
        ),
        migrations.AlterModelOptions(
            name='otherdeposits',
            options={'verbose_name': 'Other Deposit', 'verbose_name_plural': 'Other Deposits'},
        ),
        migrations.AlterModelOptions(
            name='security',
            options={'verbose_name': 'Security', 'verbose_name_plural': 'Securities'},
        ),
        migrations.AlterModelOptions(
            name='securitydeposits',
            options={'verbose_name': 'Security Deposit', 'verbose_name_plural': 'Security Deposits'},
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank_account_no',
            field=models.CharField(help_text='Unique account number for the bank.', max_length=255, unique=True, verbose_name='Bank Account Number'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank_address',
            field=models.CharField(help_text='Physical address of the bank.', max_length=255, verbose_name='Bank Address'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank_code',
            field=models.CharField(help_text='The unique code assigned to the bank.', max_length=255, verbose_name='Bank Code'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank_contact',
            field=models.CharField(help_text='Contact number for the bank.', max_length=20, verbose_name='Bank Contact Number'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank_for_security',
            field=models.BooleanField(default=False, help_text='Indicates if the bank is for security purposes.', verbose_name='Security Flag'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank_manager',
            field=models.CharField(help_text='Name of the bank manager.', max_length=255, verbose_name='Bank Manager'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank_name',
            field=models.CharField(help_text='Name of the bank.', max_length=255, verbose_name='Bank Name'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='show_on_voucher',
            field=models.BooleanField(default=False, help_text='Indicates if the bank details should be shown on vouchers.', verbose_name='Show on Voucher'),
        ),
        migrations.AlterField(
            model_name='cpfund',
            name='created_by',
            field=models.ForeignKey(help_text='User who created this CP Fund.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_funds', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='cpfund',
            name='deposited_cp_fund',
            field=models.PositiveIntegerField(help_text='Amount deposited into the CP Fund.', verbose_name='Deposited CP Fund'),
        ),
        migrations.AlterField(
            model_name='cpfund',
            name='employee',
            field=models.OneToOneField(help_text='The employee associated with this CP Fund.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cpfund', to=settings.AUTH_USER_MODEL, verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='cpfund',
            name='last_date_submitted',
            field=models.DateField(help_text='The last date when the CP Fund was submitted.', verbose_name='Last Date Submitted'),
        ),
        migrations.AlterField(
            model_name='cpfunddeposits',
            name='amount',
            field=models.PositiveIntegerField(help_text='The amount deposited to the CP fund.', verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='cpfunddeposits',
            name='cp_fund',
            field=models.ForeignKey(help_text='The CP Fund to which the deposit is made.', on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to='finance.cpfund', verbose_name='CP Fund'),
        ),
        migrations.AlterField(
            model_name='cpfunddeposits',
            name='created_by',
            field=models.ForeignKey(help_text='User who created this deposit entry.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cpfund_deposits_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='cpfunddeposits',
            name='date_paid',
            field=models.DateField(help_text='The date when the deposit was made.', verbose_name='Date Paid'),
        ),
        migrations.AlterField(
            model_name='cpfunddeposits',
            name='note',
            field=models.CharField(help_text='Any additional notes regarding the deposit.', max_length=255, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='employeearrears',
            name='arrears_amount',
            field=models.IntegerField(help_text='Total amount of arrears for the employee.', verbose_name='Arrears Amount'),
        ),
        migrations.AlterField(
            model_name='employeearrears',
            name='arrears_note',
            field=models.CharField(help_text='Notes regarding the arrears.', max_length=255, verbose_name='Arrears Note'),
        ),
        migrations.AlterField(
            model_name='employeearrears',
            name='employee',
            field=models.OneToOneField(help_text='The employee associated with these arrears.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_arrears', to=settings.AUTH_USER_MODEL, verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='eobipaid',
            name='created_by',
            field=models.ForeignKey(help_text='User who created this EOBI payment entry.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eobi_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='eobipaid',
            name='employee',
            field=models.ForeignKey(help_text='The employee for whom the EOBI payment is made.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eobi_employee', to=settings.AUTH_USER_MODEL, verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='eobipaid',
            name='eobi_date_of_joining',
            field=models.DateField(help_text='The date when the employee joined.', verbose_name='Date of Joining'),
        ),
        migrations.AlterField(
            model_name='eobipaid',
            name='month',
            field=models.DateField(help_text='The month for which the EOBI payment is made.', verbose_name='Month'),
        ),
        migrations.AlterField(
            model_name='eobipaid',
            name='total_deposit',
            field=models.FloatField(help_text='Total amount deposited for EOBI.', verbose_name='Total Deposit'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='Amount of the expense.', max_digits=10, verbose_name='Expense Amount'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(help_text='Date of the expense.', verbose_name='Expense Date'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.TextField(help_text='Detailed description of the expense.', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='title',
            field=models.CharField(help_text='Title of the expense.', max_length=255, verbose_name='Expense Title'),
        ),
        migrations.AlterField(
            model_name='incometaxrates',
            name='initial_taxable_income',
            field=models.PositiveIntegerField(help_text='The starting amount of taxable income.', verbose_name='Initial Taxable Income'),
        ),
        migrations.AlterField(
            model_name='incometaxrates',
            name='percentage',
            field=models.FloatField(help_text='The percentage of tax applied within this income bracket.', verbose_name='Tax Percentage'),
        ),
        migrations.AlterField(
            model_name='incometaxrates',
            name='session',
            field=models.ForeignKey(help_text='The session to which these tax rates apply.', on_delete=django.db.models.deletion.CASCADE, to='finance.incometaxsession', verbose_name='Income Tax Session'),
        ),
        migrations.AlterField(
            model_name='incometaxrates',
            name='to_taxable_income',
            field=models.PositiveIntegerField(help_text='The ending amount of taxable income.', verbose_name='To Taxable Income'),
        ),
        migrations.AlterField(
            model_name='incometaxsession',
            name='ending_year',
            field=models.DateField(help_text='The year when the income tax session ends.', verbose_name='Ending Year'),
        ),
        migrations.AlterField(
            model_name='incometaxsession',
            name='starting_year',
            field=models.DateField(help_text='The year when the income tax session starts.', verbose_name='Starting Year'),
        ),
        migrations.AlterField(
            model_name='installmentpaid',
            name='amount_paid',
            field=models.FloatField(help_text='Amount of the installment that has been paid.', verbose_name='Amount Paid'),
        ),
        migrations.AlterField(
            model_name='installmentpaid',
            name='date_paid',
            field=models.DateField(help_text='The date when the installment was paid.', verbose_name='Date Paid'),
        ),
        migrations.AlterField(
            model_name='installmentpaid',
            name='loan',
            field=models.ForeignKey(help_text='The loan for which the installment is paid.', on_delete=django.db.models.deletion.CASCADE, to='finance.loan', verbose_name='Loan'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='employee',
            field=models.ForeignKey(help_text='The employee who has taken the loan.', on_delete=django.db.models.deletion.CASCADE, to='employee.employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_amount',
            field=models.FloatField(help_text='Total amount of the loan taken.', verbose_name='Loan Amount'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='remaining_amount',
            field=models.FloatField(help_text='Amount still outstanding on the loan.', verbose_name='Remaining Amount'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='total_installments',
            field=models.PositiveIntegerField(help_text='Total number of installments for repayment.', verbose_name='Total Installments'),
        ),
        migrations.AlterField(
            model_name='monthclosing',
            name='bank',
            field=models.ForeignKey(help_text='The bank associated with this month closing.', on_delete=django.db.models.deletion.CASCADE, related_name='month_closings', to='finance.bank', verbose_name='Bank'),
        ),
        migrations.AlterField(
            model_name='monthclosing',
            name='month',
            field=models.DateField(help_text='The month for which the closing is calculated.', verbose_name='Closing Month'),
        ),
        migrations.AlterField(
            model_name='monthclosing',
            name='profit_by_bank',
            field=models.PositiveIntegerField(help_text='The profit calculated for this month closing.', verbose_name='Profit'),
        ),
        migrations.AlterField(
            model_name='otherdeposits',
            name='amount',
            field=models.PositiveIntegerField(help_text='The amount deposited to the bank.', verbose_name='Deposit Amount'),
        ),
        migrations.AlterField(
            model_name='otherdeposits',
            name='bank',
            field=models.ForeignKey(help_text='The bank where the deposit is made.', on_delete=django.db.models.deletion.CASCADE, related_name='other_deposits', to='finance.bank', verbose_name='Bank'),
        ),
        migrations.AlterField(
            model_name='otherdeposits',
            name='date',
            field=models.DateField(help_text='The date when the deposit was made.', verbose_name='Deposit Date'),
        ),
        migrations.AlterField(
            model_name='otherdeposits',
            name='remarks',
            field=models.CharField(help_text='Any additional remarks regarding the deposit.', max_length=255, verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='security',
            name='created_by',
            field=models.ForeignKey(help_text='Employee who created this security entry.', on_delete=django.db.models.deletion.CASCADE, related_name='created_security', to='employee.employee', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='security',
            name='deposited_security',
            field=models.PositiveIntegerField(help_text='Amount deposited as security.', verbose_name='Deposited Security'),
        ),
        migrations.AlterField(
            model_name='security',
            name='employee',
            field=models.OneToOneField(help_text='The employee associated with this security deposit.', on_delete=django.db.models.deletion.CASCADE, related_name='employee_security', to='employee.employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='security',
            name='last_date_submitted',
            field=models.DateField(help_text='The last date when the security deposit was made.', verbose_name='Last Date Submitted'),
        ),
        migrations.AlterField(
            model_name='security',
            name='total_security',
            field=models.PositiveIntegerField(help_text='Total security amount deposited.', verbose_name='Total Security'),
        ),
        migrations.AlterField(
            model_name='securitydeposits',
            name='amount',
            field=models.PositiveIntegerField(help_text='The amount deposited as security.', verbose_name='Deposit Amount'),
        ),
        migrations.AlterField(
            model_name='securitydeposits',
            name='created_by',
            field=models.ForeignKey(help_text='Employee who created this security deposit entry.', on_delete=django.db.models.deletion.CASCADE, related_name='created_security_deposits', to='employee.employee', verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='securitydeposits',
            name='date_paid',
            field=models.DateField(help_text='The date when the security deposit was made.', verbose_name='Date Paid'),
        ),
        migrations.AlterField(
            model_name='securitydeposits',
            name='note',
            field=models.CharField(help_text='Any additional notes regarding the security deposit.', max_length=255, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='securitydeposits',
            name='security',
            field=models.ForeignKey(help_text='The security associated with this deposit.', on_delete=django.db.models.deletion.CASCADE, related_name='security_deposits', to='finance.security', verbose_name='Security'),
        ),
        migrations.AlterUniqueTogether(
            name='incometaxrates',
            unique_together={('session', 'initial_taxable_income', 'to_taxable_income')},
        ),
        migrations.AlterUniqueTogether(
            name='monthclosing',
            unique_together={('bank', 'month')},
        ),
        migrations.AddIndex(
            model_name='bank',
            index=models.Index(fields=['bank_name'], name='bank_name_idx'),
        ),
        migrations.AddIndex(
            model_name='cpfund',
            index=models.Index(fields=['employee'], name='cpf_employee_idx'),
        ),
        migrations.AddIndex(
            model_name='cpfunddeposits',
            index=models.Index(fields=['cp_fund'], name='cpf_deposit_fund_idx'),
        ),
        migrations.AddIndex(
            model_name='cpfunddeposits',
            index=models.Index(fields=['date_paid'], name='cpf_deposit_date_idx'),
        ),
        migrations.AddIndex(
            model_name='eobipaid',
            index=models.Index(fields=['employee'], name='eobi_employee_idx'),
        ),
        migrations.AddIndex(
            model_name='eobipaid',
            index=models.Index(fields=['month'], name='eobi_month_idx'),
        ),
        migrations.AddIndex(
            model_name='expense',
            index=models.Index(fields=['date'], name='expense_date_idx'),
        ),
        migrations.AddIndex(
            model_name='incometaxrates',
            index=models.Index(fields=['session'], name='income_tax_session_idx'),
        ),
        migrations.AddIndex(
            model_name='incometaxsession',
            index=models.Index(fields=['starting_year'], name='income_tax_start_idx'),
        ),
        migrations.AddIndex(
            model_name='installmentpaid',
            index=models.Index(fields=['loan'], name='installment_loan_idx'),
        ),
        migrations.AddIndex(
            model_name='installmentpaid',
            index=models.Index(fields=['date_paid'], name='installment_date_idx'),
        ),
        migrations.AddIndex(
            model_name='loan',
            index=models.Index(fields=['employee'], name='loan_employee_idx'),
        ),
        migrations.AddIndex(
            model_name='monthclosing',
            index=models.Index(fields=['bank'], name='month_closing_bank_idx'),
        ),
        migrations.AddIndex(
            model_name='monthclosing',
            index=models.Index(fields=['month'], name='month_closing_month_idx'),
        ),
        migrations.AddIndex(
            model_name='otherdeposits',
            index=models.Index(fields=['bank'], name='other_deposit_bank_idx'),
        ),
        migrations.AddIndex(
            model_name='otherdeposits',
            index=models.Index(fields=['date'], name='other_deposit_date_idx'),
        ),
        migrations.AddIndex(
            model_name='security',
            index=models.Index(fields=['employee'], name='security_employee_idx'),
        ),
        migrations.AddIndex(
            model_name='securitydeposits',
            index=models.Index(fields=['security'], name='security_deposit_security_idx'),
        ),
        migrations.AddIndex(
            model_name='securitydeposits',
            index=models.Index(fields=['date_paid'], name='security_deposit_date_idx'),
        ),
        migrations.AddConstraint(
            model_name='incometaxsession',
            constraint=models.CheckConstraint(check=models.Q(('starting_year__lt', 'ending_year')), name='starting_year_before_ending_year'),
        ),
    ]
