
from openerp import api
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date, time, timedelta, datetime



class custom_script(osv.osv):
    _name = "custom.script"

    @api.multi
    def worked_hours_compute(self,context=None):

        res = 1.00
        # ### Custom Funcition
        vals_parameter = [('state', '=', 'activated'), ('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        # vals_parameter = [('state', '=', 'activated'), ('create_date', '>=', '2021-10-31 23:54:38.048066'),('create_date', '<=', '2021-11-30 23:53:42.652096')]
        # vals_parameter = [('state', '=', 'activated'), ('create_date', '>=', '2021-11-30 23:54:38.048066'),('create_date', '<=', '2021-12-31 23:53:42.652096')]
        # vals_parameter = [('state', '=', 'activated'), ('create_date', '>=', '2021-12-31 23:54:38.048066'),('create_date', '<=', '2022-01-31 23:53:42.652096')]
        # vals_parameter = [('state', '=', 'activated'), ('create_date', '>=', '2021-01-31 23:54:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['leih.admission'].search(vals_parameter)
        for stored_obj in mr_obj:
            line_ids = []

            # if context is None: context = {}
            # if context.get('period_id', False):
            #     return context.get('period_id')
            # periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            # period_id = periods and periods[0] or False


            #new code
            if context is None: context = {}
            if context.get('period_id', False):
                return context.get('period_id')
            periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            period_id = periods and periods[0] or False
            dates=stored_obj.date
            dt = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S")
            if dt.month==2:
                period_id=29
            if dt.month==1:
                period_id=28
            if dt.month==12:
                period_id=27
            if dt.month==11:
                period_id=26
            if dt.month==10:
                period_id=25
            if dt.month==9:
                period_id=24
            if dt.month==8:
                period_id=23
            if dt.month==7:
                period_id=22
            if dt.month==6:
                period_id=22
            #end
            ar_amount = stored_obj.due
            has_been_paid=stored_obj.paid

            if ar_amount > 0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': stored_obj.name,
                    'currency_id': False,
                    'credit': 0,
                    'date_maturity': False,
                    'account_id': 195,  ### Accounts Receivable ID
                    'debit': ar_amount,
                    'amount_currency': 0,
                    'partner_id': False,
                }))

            if has_been_paid > 0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': stored_obj.name,
                    'currency_id': False,
                    'credit': 0,
                    'date_maturity': False,
                    'account_id': 6,  ### Cash ID
                    'debit': has_been_paid,
                    'amount_currency': 0,
                    'partner_id': False,
                }))

            for cc_obj in stored_obj.leih_admission_line_id:
                total=0

                if cc_obj.name.name:
                    ledger_id = 611
                    try:
                        ledger_id = cc_obj.name.accounts_id.id
                    except:
                        ledger_id = 611  ## Diagnostic Income Head , If we don't assign any Ledger

                    if context is None:
                        context = {}

                    line_ids.append((0, 0, {
                        'analytic_account_id': False,
                        'tax_code_id': False,
                        'tax_amount': 0,
                        'name': cc_obj.name.name,
                        'currency_id': False,
                        'account_id': cc_obj.name.accounts_id.id,
                        'credit': cc_obj.total_amount,
                        'date_maturity': False,
                        'debit': 0,
                        'amount_currency': 0,
                        'partner_id': False,
                    }))
                # import pdb
                # pdb.set_trace()


            jv_entry = self.pool.get('account.move')

            j_vals = {'name': '/',
                      'journal_id': 2,  ## Sales Journal
                      'date': stored_obj.date,
                      'period_id': period_id,
                      'ref': stored_obj.name,
                      'line_id': line_ids

                      }

            # import pdb
            # pdb.set_trace()

            saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
            if saved_jv_id > 0:
                journal_id = saved_jv_id
                try:
                    jv_entry.button_validate(self.env.cr, self.env.uid, [saved_jv_id], context)
                except:
                    import pdb
                    pdb.set_trace()
                # self.cr.execute("update leih_admission set old_journal=True where id=%s", (stored_obj.name.id))
                # self.cr.commit()

        return res

    # , ('create_date', '<=', '2021-07-30 05:50:16.243824')
    # ('create_date', '=', '2021-11-16 10:14:03.963665')
###bill regsiter_button
    @api.multi
    def bill_compute(self, context=None):

        res = 1.00
        # ### Custom Funcition ('create_date', '<=', '2022-02-25 07:53:42.652096')
        # vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2021-10-31 23:53:42.652096')]
        # vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-10-31 23:54:38.048066'),('create_date', '<=', '2021-11-30 23:53:42.652096')]
        # vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-11-30 23:54:38.048066'),('create_date', '<=', '2021-12-31 23:53:42.652096')]
        vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-12-31 23:54:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        # vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-01-31 23:54:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]


        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['bill.register'].search(vals_parameter)
        for stored_obj in mr_obj:
            line_ids = []

            # if context is None: context = {}
            # if context.get('period_id', False):
            #     return context.get('period_id')
            # periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            # period_id = periods and periods[0] or False
            #new code
            if context is None: context = {}
            if context.get('period_id', False):
                return context.get('period_id')
            periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            period_id = periods and periods[0] or False
            has_been_paid = stored_obj.paid
            dates=stored_obj.date
            dt = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S")
            if dt.month==2:
                period_id=29
            if dt.month==1:
                period_id=28
            if dt.month==12:
                period_id=27
            if dt.month==11:
                period_id=26
            if dt.month==10:
                period_id=25
            if dt.month==9:
                period_id=24
            if dt.month==8:
                period_id=23
            if dt.month==7:
                period_id=22
            if dt.month==6:
                period_id=22
            #end

            ar_amount = stored_obj.due
            has_been_paid = stored_obj.paid

            if ar_amount > 0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': stored_obj.name,
                    'currency_id': False,
                    'credit': 0,
                    'date_maturity': False,
                    'account_id': 195,  ### Accounts Receivable ID
                    'debit': ar_amount,
                    'amount_currency': 0,
                    'partner_id': False,
                }))

            if has_been_paid > 0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': stored_obj.name,
                    'currency_id': False,
                    'credit': 0,
                    'date_maturity': False,
                    'account_id': 6,  ### Cash ID
                    'debit': has_been_paid,
                    'amount_currency': 0,
                    'partner_id': False,
                }))

            for cc_obj in stored_obj.bill_register_line_id:
                total = 0

                if cc_obj.name.name:
                    ledger_id = 611
                    try:
                        ledger_id = cc_obj.name.accounts_id.id
                    except:
                        ledger_id = 611  ## Diagnostic Income Head , If we don't assign any Ledger

                    if context is None:
                        context = {}
                    # if cc_obj.name.accounts_id.type=='View':
                    #     import pdb
                    #     pdb.set_trace()

                    line_ids.append((0, 0, {
                        'analytic_account_id': False,
                        'tax_code_id': False,
                        'tax_amount': 0,
                        'name': cc_obj.name.name,
                        'currency_id': False,
                        'account_id': cc_obj.name.accounts_id.id,
                        'credit': cc_obj.total_amount,
                        'date_maturity': False,
                        'debit': 0,
                        'amount_currency': 0,
                        'partner_id': False,
                    }))
                # import pdb
                # pdb.set_trace()

            jv_entry = self.pool.get('account.move')

            j_vals = {'name': '/',
                      'journal_id': 2,  ## Sales Journal
                      'date': stored_obj.date,
                      'period_id': period_id,
                      'ref': stored_obj.name,
                      'line_id': line_ids
                      }

            # import pdb
            # pdb.set_trace()

            try:
                saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
            except:
                import pdb
                pdb.set_trace()
            if saved_jv_id > 0:
                journal_id = saved_jv_id
                try:

                    jv_entry.button_validate(self.env.cr, self.env.uid, [saved_jv_id], context)
                except:
                    import pdb
                    pdb.set_trace()
                # self.cr.execute("update leih_admission set old_journal=True where id=%s", (stored_obj.name.id))
                # self.cr.commit()

        # print("## ############################## ")
        # print(mr_obj)

        # 1. Bill date search diben
        # Er journal diebn lopp fele
        #
        return res



    ###OPtics journal entries
    @api.multi
    def optics_journal(self, context=None):

        res = 1.00
        # ### Custom Funcition
        # vals_parameter = [('state', '=', 'confirmed'), ('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2021-11-30 23:53:42.652096')]
        vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-11-30 23:54:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]

        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['optics.sale'].search(vals_parameter)
        for stored_obj in mr_obj:
            line_ids = []

            # if context is None: context = {}
            # if context.get('period_id', False):
            #     return context.get('period_id')
            # periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            # period_id = periods and periods[0] or False

            #new code for period
            if context is None: context = {}
            if context.get('period_id', False):
                return context.get('period_id')
            periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            period_id = periods and periods[0] or False
            dates=stored_obj.date
            dt = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S")
            if dt.month==2:
                period_id=29
            if dt.month==1:
                period_id=28
            if dt.month==12:
                period_id=27
            if dt.month==11:
                period_id=26
            if dt.month==10:
                period_id=25
            if dt.month==9:
                period_id=24
            if dt.month==8:
                period_id=23
            if dt.month==7:
                period_id=22
            if dt.month==6:
                period_id=22
            #end
            ar_amount = stored_obj.due
            has_been_paid = stored_obj.paid

            if ar_amount > 0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': stored_obj.name,
                    'currency_id': False,
                    'credit': 0,
                    'date_maturity': False,
                    'account_id': 6099,  ### Accounts Receivable for optics ID
                    'debit': ar_amount,
                    'amount_currency': 0,
                    'partner_id': False,
                }))

            if has_been_paid > 0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': stored_obj.name,
                    'currency_id': False,
                    'credit': 0,
                    'date_maturity': False,
                    'account_id': 6,  ### Cash ID
                    'debit': has_been_paid,
                    'amount_currency': 0,
                    'partner_id': False,
                }))

                if context is None:
                    context = {}

            if stored_obj.total:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': stored_obj.name,
                    'currency_id': False,
                    'account_id': 6098,
                    'credit': stored_obj.total,
                    'date_maturity': False,
                    'debit': 0,
                    'amount_currency': 0,
                    'partner_id': False,
                }))

            jv_entry = self.pool.get('account.move')

            j_vals = {'name': '/',
                      'journal_id': 2,  ## Sales Journal
                      'date': stored_obj.date,
                      'period_id': period_id,
                      'ref': stored_obj.name,
                      'line_id': line_ids

                      }

            # import pdb
            # pdb.set_trace()

            # import pdb
            # pdb.set_trace()

            saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
            if saved_jv_id > 0:
                journal_id = saved_jv_id
                try:

                    jv_entry.button_validate(self.env.cr, self.env.uid, [saved_jv_id], context)
                except:
                    import pdb
                    pdb.set_trace()
                # self.cr.execute("update leih_admission set old_journal=True where id=%s", (stored_obj.name.id))
                # self.cr.commit()

        # print("## ############################## ")
        # print(mr_obj)

        # 1. Bill date search diben
        # Er journal diebn lopp fele
        #
        return res
    ###End of optics journal




    ###OPD Journal
    @api.multi
    def opd_journal(self, context=None):

        res = 1.00
        # ### Custom Funcition
        # vals_parameter = [('state','!=','cancelled'), ('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2021-10-31 23:53:42.652096')]
        # vals_parameter = [('state','!=','cancelled'),('create_date', '>=', '2021-10-31 23:54:38.048066'),('create_date', '<=', '2021-11-30 23:53:42.652096')]
        # vals_parameter = [('state','!=','cancelled'),('create_date', '>=', '2021-11-30 23:54:38.048066'),('create_date', '<=', '2021-12-31 23:53:42.652096')]
        # vals_parameter = [('state','!=','cancelled'),('create_date', '>=', '2021-12-31 23:54:38.048066'),('create_date', '<=', '2022-01-31 23:53:42.652096')]
        vals_parameter = [('state','!=','cancelled'),('create_date', '>=', '2022-01-31 23:54:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['opd.ticket'].search(vals_parameter)
        for stored_obj in mr_obj:
            line_ids = []

            if context is None: context = {}

            #new code
            if context is None: context = {}
            if context.get('period_id', False):
                return context.get('period_id')
            periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            period_id = periods and periods[0] or False
            dates=stored_obj.date
            dt = datetime.strptime(dates, '%Y-%m-%d')
            if dt.month==2:
                period_id=29
            if dt.month==1:
                period_id=28
            if dt.month==12:
                period_id=27
            if dt.month==11:
                period_id=26
            if dt.month==10:
                period_id=25
            if dt.month==9:
                period_id=24
            if dt.month==8:
                period_id=23
            if dt.month==7:
                period_id=22
            if dt.month==6:
                period_id=22
            #end
            has_been_paid = stored_obj.total



            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': stored_obj.name,
                'currency_id': False,
                'credit': 0,
                'date_maturity': False,
                'account_id': 6,  ### Cash ID
                'debit': has_been_paid,
                'amount_currency': 0,
                'partner_id': False,
            }))

            for cc_obj in stored_obj.opd_ticket_line_id:
                # import pdb
                # pdb.set_trace()
                total = 0

                if cc_obj.name.name:
                    # ledger_id = 611
                    # try:
                    #     ledger_id = cc_obj.name.accounts_id.id
                    # except:
                    #     ledger_id = 611  ## Diagnostic Income Head , If we don't assign any Ledger

                    if context is None:
                        context = {}

                    line_ids.append((0, 0, {
                        'analytic_account_id': False,
                        'tax_code_id': False,
                        'tax_amount': 0,
                        'name': cc_obj.name.name,
                        'currency_id': False,
                        'account_id': cc_obj.name.accounts_id.id,
                        'credit': cc_obj.total_amount,
                        'date_maturity': False,
                        'debit': 0,
                        'amount_currency': 0,
                        'partner_id': False,
                    }))
                # import pdb
                # pdb.set_trace()

            jv_entry = self.pool.get('account.move')

            j_vals = {'name': '/',
                      'journal_id': 2,  ## Sales Journal
                      'date': stored_obj.date,
                      'period_id': period_id,
                      'ref': stored_obj.name,
                      'line_id': line_ids
                      }

            saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
            if saved_jv_id > 0:
                journal_id = saved_jv_id
                try:
                    jv_entry.button_validate(self.env.cr, self.env.uid, [saved_jv_id], context)
                except:
                    import pdb
                    pdb.set_trace()
                # self.cr.execute("update leih_admission set old_journal=True where id=%s", (stored_obj.name.id))
                # self.cr.commit()

        # print("## ############################## ")
        # print(mr_obj)

        # 1. Bill date search diben
        # Er journal diebn lopp fele
        #
        return res


    @api.multi
    def delete_journal(self,context=None):
        vals_parameter=[('create_date','>=','2022-02-10 04:00:00.048066'),('create_date','<=','2022-06-11 01:30:00.048066'),('ref','like','OPD'),('date','<','2022-02-01')]
        opd_obj=self.env['account.move'].search(vals_parameter)
        xx = opd_obj.button_cancel()
        opd_obj.unlink()
        return 'X'

    ###OPD Journal End

    @api.multi
    def weighted_distribution_cal(self,context=None):
        # vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-07-01 04:46:56.269666'), ('create_date', '<=', '2021-07-31 13:18:37.700759')]
        vals_parameter = [('state', '=', 'activated'),('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]

        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['leih.admission'].search(vals_parameter)
        # import pdb
        # pdb.set_trace()
        for bill_item in mr_obj:
            item_ids=[]
            doctors_discount=0
            total=0

            if bill_item.doctors_discounts > 0:
                doctors_discount=round((bill_item.total*bill_item.doctors_discounts)/100)
            if bill_item.other_discount>0 and bill_item.other_discount>doctors_discount:
                factor_total=bill_item.total
                factor_other_discount=bill_item.other_discount
                factor_doctor_discount=bill_item.doctors_discounts
                if factor_total>0:
                    multiply_result=factor_other_discount/factor_total
                    factor_multiply=1-multiply_result
                    for item in bill_item.leih_admission_line_id:
                        item.total_amount=round(item.price*factor_multiply)
                        item.flat_discount=item.price*multiply_result
                        item.total_discount=item.flat_discount+item.discount_percent
                        total = total + item.total_amount
                        item_ids.append(item.id)


            elif doctors_discount>bill_item.other_discount:
                factor_total = bill_item.total
                factor_other_discount = doctors_discount
                multiply_result = factor_other_discount / factor_total
                factor_multiply = 1 - multiply_result
                for item in bill_item.leih_admission_line_id:
                    item.total_amount = round(item.price * factor_multiply)
                    item.flat_discount = item.price * multiply_result
                    item.total_discount = item.flat_discount + item.discount_percent
                    bill_item.other_discount=0
                    total = total + item.total_amount
            if bill_item.other_discount > 0 or bill_item.doctors_discounts > 0:
                if total!=factor_total-factor_other_discount-doctors_discount:
                    bill_total=factor_total-factor_other_discount-doctors_discount
                    total_difference=bill_total-total
                    if len(item_ids)>0:
                        item_id=item_ids[0]
                        bill_line_obj = self.env['leih.admission.line'].search([('id', '=', item_id)], limit=1)
                        for item in bill_line_obj:
                            item.total_amount=item.total_amount+total_difference

        return True


    ###Weighted distribution for bill register
    @api.multi
    def bill_weighted_distribution(self, context=None):
        # vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-07-01 04:46:56.269666'), ('create_date', '<=', '2021-07-31 13:18:37.700759')]
        vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]

        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['bill.register'].search(vals_parameter)
        # import pdb
        # pdb.set_trace()
        for bill_item in mr_obj:
            item_ids = []
            doctors_discount = 0
            total = 0

            if bill_item.doctors_discounts > 0:
                doctors_discount = round((bill_item.total_without_discount * bill_item.doctors_discounts) / 100)
            if bill_item.other_discount > 0 and bill_item.other_discount > doctors_discount:
                factor_total = bill_item.total_without_discount
                factor_other_discount = bill_item.other_discount
                factor_doctor_discount = bill_item.doctors_discounts
                if factor_total > 0:
                    multiply_result = factor_other_discount / factor_total
                    factor_multiply = 1 - multiply_result
                    for item in bill_item.bill_register_line_id:
                        item.total_amount = round(item.price * factor_multiply)
                        item.flat_discount = item.price * multiply_result
                        item.total_discount = item.flat_discount + item.discount_percent
                        total = total + item.total_amount
                        item_ids.append(item.id)


            elif doctors_discount > bill_item.other_discount:
                factor_total = bill_item.total_without_discount
                factor_other_discount = doctors_discount
                multiply_result = factor_other_discount / factor_total
                factor_multiply = 1 - multiply_result
                for item in bill_item.bill_register_line_id:
                    item.total_amount = round(item.price * factor_multiply)
                    item.flat_discount = item.price * multiply_result
                    item.total_discount = item.flat_discount + item.discount_percent
                    # import pdb
                    # pdb.set_trace()

                    try:
                        bill_item.other_discount = 0
                        total = total + item.total_amount
                    except:
                        import pdb
                        pdb.set_trace()
            if bill_item.other_discount>0 or bill_item.doctors_discounts>0:
                doctors_discounts=(factor_total*doctors_discount)/100
                if total != factor_total - factor_other_discount - doctors_discounts:
                    bill_total = factor_total - factor_other_discount - doctors_discounts
                    total_difference = bill_total - total
                    # import pdb
                    # pdb.set_trace()
                    if len(item_ids) > 0:
                        item_id = item_ids[0]
                        bill_line_obj = self.env['bill.register.line'].search([('id', '=', item_id)], limit=1)
                        for item in bill_line_obj:
                            item.total_amount = item.total_amount + total_difference

        return True



    ###Check Bill Total and item total
    @api.multi
    def check_bill(self, context=None):
        # vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        # mr_obj = self.env['bill.register'].search(vals_parameter)
        # bill_no=[]
        # for bill_item in mr_obj:
        #     item_ids = []
        #     doctors_discount = 0
        #     total = 0
        #     for item in bill_item.bill_register_line_id:
        #         total = total + item.total_amount
        #     if total!=bill_item.grand_total:
        #         bill_no.append(bill_item.name)
        #for admission->
        vals_parameter = [('state', '=', 'activated'), ('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        mr_obj = self.env['leih.admission'].search(vals_parameter)
        bill_no=[]
        for bill_item in mr_obj:
            item_ids = []
            doctors_discount = 0
            total = 0
            for item in bill_item.leih_admission_line_id:
                total = total + item.total_amount
            if total!=bill_item.grand_total:
                bill_no.append(bill_item.name)

        import pdb
        pdb.set_trace()


        return True



    def _worked_hour_compute(self):

        return 'X'

    _columns = {

        # 'worked_hours': fields.function(_worked_hour_compute, type='float', string='Worked Hours', store=True),
        'worked_hours': fields.char("Nothin"),
        # 'worked_hours': fields.function(_worked_hours_compute, type='float', string='Worked Hours', store=True),


    }

    @api.multi
    def discount_journal(self, context=None):

        res = 1.00
        # ### Custom Funcition
        vals_parameter = [('create_date', '<=', '2022-04-02 00:00:00.719471'),('state', '=', 'approve')]
        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['discount'].search(vals_parameter)
        # import pdb
        # pdb.set_trace()
        for stored_obj in mr_obj:
            line_ids = []

            if context is None: context = {}
            if context.get('period_id', False):
                return context.get('period_id')
            periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            period_id = periods and periods[0] or False
            has_been_paid = stored_obj.total

            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': stored_obj.name,
                'currency_id': False,
                'credit': 0,
                'date_maturity': False,
                'account_id': 6,  ### Cash ID
                'debit': has_been_paid,
                'amount_currency': 0,
                'partner_id': False,
            }))

            for cc_obj in stored_obj.opd_ticket_line_id:
                # import pdb
                # pdb.set_trace()
                total = 0

                if cc_obj.name.name:
                    # ledger_id = 611
                    # try:
                    #     ledger_id = cc_obj.name.accounts_id.id
                    # except:
                    #     ledger_id = 611  ## Diagnostic Income Head , If we don't assign any Ledger

                    if context is None:
                        context = {}

                    line_ids.append((0, 0, {
                        'analytic_account_id': False,
                        'tax_code_id': False,
                        'tax_amount': 0,
                        'name': cc_obj.name.name,
                        'currency_id': False,
                        'account_id': cc_obj.name.accounts_id.id,
                        'credit': cc_obj.total_amount,
                        'date_maturity': False,
                        'debit': 0,
                        'amount_currency': 0,
                        'partner_id': False,
                    }))
                # import pdb
                # pdb.set_trace()

            jv_entry = self.pool.get('account.move')

            j_vals = {'name': '/',
                      'journal_id': 2,  ## Sales Journal
                      'date': stored_obj.date,
                      'period_id': 24,
                      'ref': stored_obj.name,
                      'line_id': line_ids

                      }

            saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
            if saved_jv_id > 0:
                journal_id = saved_jv_id
                try:

                    jv_entry.button_validate(self.env.cr, self.env.uid, [saved_jv_id], context)
                except:
                    import pdb
                    pdb.set_trace()
                # self.cr.execute("update leih_admission set old_journal=True where id=%s", (stored_obj.name.id))
                # self.cr.commit()

        # print("## ############################## ")
        # print(mr_obj)

        # 1. Bill date search diben
        # Er journal diebn lopp fele
        #
        return res

    @api.multi
    def ipe_correction(self, context=None):
        vals_parameter = [('create_date', '<=', '2022-02-25 07:53:42.652096'),('ref','like','IPE')]
        ipr_obj = self.env['account.move'].search(vals_parameter)
        ipr_obj.button_cancel()
        ipr_obj.unlink()
        return True

    @api.multi
    def ir_correction(self, context=None):
        vals_parameter = [('create_date', '<=', '2022-02-25 07:53:42.652096'),('ref','like','IR')]
        ir_obj = self.env['account.move'].search(vals_parameter)

        return True
    @api.multi
    def ipe_journal(self, context=None):
        vals_parameter = [('create_date', '<=', '2022-02-25 07:53:42.652096'),('state','=','confirmed')]
        ipe_obj = self.env['inventory.product.entry'].search(vals_parameter)
        for stored_obj in ipe_obj:
            name=str(stored_obj.name)
            partner_id=stored_obj.partner_id.id
            creditors_acc=stored_obj.partner_id.property_account_payable.id
            total_amount=stored_obj.total
            # product_id=stored_obj.inventory_product_entry_line_ids.product_name.id
            # product = self.env['product.product'].search([('id', '=', product_id)])
            # unit_amount = product.price_get('standard_price')[product.id]
            line_ids = []

            if context is None: context = {}
            if context.get('period_id', False):
                return context.get('period_id')
            periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            period_id = periods and periods[0] or False
            dates=stored_obj.date
            dt = datetime.strptime(dates, '%Y-%m-%d')
            if dt.month==2:
                period_id=29
            if dt.month==1:
                period_id=28
            if dt.month==12:
                period_id=27
            if dt.month==11:
                period_id=26
            if dt.month==10:
                period_id=25
            if dt.month==9:
                period_id=24
            if dt.month==8:
                period_id=23
            if dt.month==7:
                period_id=22
            if dt.month==6:
                period_id=22
            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': name,
                'currency_id': False,
                'account_id': creditors_acc,
                'credit': total_amount,
                'date_maturity': False,
                'debit': 0,
                'amount_currency': 0,
                'partner_id': partner_id,
            }))

            for cc_obj in stored_obj.inventory_product_entry_line_ids:

                stock_account=cc_obj.product_name.categ_id.property_stock_valuation_account_id.id
                total_price=cc_obj.total_price

                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': name,
                    'currency_id': False,
                    'account_id': stock_account,
                    'credit': 0,
                    'date_maturity': False,
                    'debit': total_price,
                    'amount_currency': 0,
                    'partner_id': partner_id,
                }))

            jv_entry = self.pool.get('account.move')

            j_vals = {'name': '/',
                      'journal_id': 6,  ## Sales Journal
                      'date': stored_obj.date,
                      'period_id': period_id,
                      'ref': name,
                      'line_id': line_ids
                      }
            try:
                saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
            except:
                import pdb
                pdb.set_trace()
        return True

    @api.multi
    def updtae_cost_price_from_ipe(self):
        vals_parameter = [('standard_price', '=', 0.00)]
        p_obj = self.env['product.product'].search(vals_parameter)
        get_all_ids = [itm.id for itm in p_obj]

        for id in get_all_ids:
            query = "select inventory_product_entry_line.unit_price from inventory_product_entry_line,inventory_product_entry " \
                    "where inventory_product_entry_line.inventory_product_entry_id=inventory_product_entry.id and " \
                    "state='confirmed' and inventory_product_entry_line.product_name=%s " \
                    "order by inventory_product_entry_line.id desc limit 1"

            self.env.cr.execute(query,([id]))
            cost_lsts = self.env.cr.fetchall()
            cost_price = 0.0
            if len(cost_lsts)>0:
                cost_price = cost_lsts[0][0]
                p_obj = self.env['product.product'].search([('id','=',id)])
                p_obj.standard_price=cost_price
            else:
                query = "select purchase_order_line.price_unit from purchase_order_line,purchase_order " \
                        "where purchase_order_line.order_id=purchase_order.id and " \
                        "purchase_order.state='approved' and purchase_order_line.product_id=%s " \
                        "order by purchase_order_line.id desc limit 1"

                self.env.cr.execute(query, ([id]))
                cost_lsts = self.env.cr.fetchall()
                cost_price = 0.0
                if len(cost_lsts) > 0:
                    cost_price = cost_lsts[0][0]
                    p_obj = self.env['product.product'].search([('id', '=', id)])
                    p_obj.standard_price = cost_price

                # self.env.cr.execute('update product_template set standard_price=%s where id=%s', (cost_price, id))
                # self.env.cr.commit()


        return True

    @api.multi
    def ir_journal(self, context=None):
        vals_parameter = [('create_date', '<=', '2022-02-25 07:53:42.652096'),('state','=','confirmed')]
        ir_obj = self.env['inventory.requisition'].search(vals_parameter)

        for stored_obj in ir_obj:
            name = str(stored_obj.name)
            # product_id=stored_obj.inventory_product_entry_line_ids.product_name.id
            # product = self.env['product.product'].search([('id', '=', product_id)])
            # unit_amount = product.price_get('standard_price')[product.id]
            line_ids = []

            if context is None: context = {}
            if context.get('period_id', False):
                return context.get('period_id')
            periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            period_id = periods and periods[0] or False
            dates = stored_obj.date
            dt = datetime.strptime(dates, '%Y-%m-%d')
            if dt.month == 2:
                period_id = 29
            if dt.month == 1:
                period_id = 28
            if dt.month == 12:
                period_id = 27
            if dt.month == 11:
                period_id = 26
            if dt.month == 10:
                period_id = 25
            if dt.month == 9:
                period_id = 24
            if dt.month == 8:
                period_id = 23
            if dt.month == 7:
                period_id = 22
            if dt.month == 6:
                period_id = 22

            for cc_obj in stored_obj.inventory_requisition_line_ids:
                stock_account = cc_obj.product_name.categ_id.property_stock_valuation_account_id.id
                cogs_account = cc_obj.product_name.categ_id.property_account_expense_categ.id
                cost_price = cc_obj.product_name.standard_price

                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': name,
                    'currency_id': False,
                    'account_id': stock_account,
                    'credit': cost_price,
                    'date_maturity': False,
                    'debit': 0,
                    'amount_currency': 0,

                }))


                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': name,
                    'currency_id': False,
                    'account_id': cogs_account,
                    'credit': 0,
                    'date_maturity': False,
                    'debit': cost_price,
                    'amount_currency': 0,
                }))

            jv_entry = self.pool.get('account.move')

            j_vals = {'name': '/',
                      'journal_id': 6,  ## Sales Journal
                      'date': stored_obj.date,
                      'period_id': period_id,
                      'ref': name,
                      'line_id': line_ids
                      }
            try:
                saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
            except:
                pass

        return True

    @api.multi
    def update_purchase_stock(self,context=None):

        # vals_parameter = [('date_invoice', '<=', '2022-02-25 07:53:42.652096'), ('type', '=', 'in_invoice'),('state','=','open')]
        # inv_obj = self.env['account.invoice'].search(vals_parameter)

        update_list = []

        inv_list = [1 ,3 ,5 ,6 ,7 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,27 ,28 ,29 ,36 ,37 ,38 ,39 ,40 ,41 ,42 ,43 ,44 ,45 ,46 ,47 ,49 ,50 ,51 ,52 ,54 ,55 ,56]
        proxy = self.pool['account.invoice']

        source_dict = {}

        for itms in proxy.browse(self.env.cr, self.env.uid, inv_list, context=context):

            inv_list.append(itms.id)
            source_dict[itms.id]=itms.origin
            for line_itm in itms.invoice_line:
                update_list.append((line_itm.product_id.categ_id.property_stock_valuation_account_id.id,line_itm.id))


        for list_itms in update_list:
            update_query = "update account_invoice_line set account_id=%s where id=%s"
            self.env.cr.execute(update_query,list_itms)
            self.env.cr.commit()

        for inv_id,pick_name in source_dict.iteritems():

            if inv_id not in [53,35,34,33,31,30,8,4]:

                get_date_done_date = "select date(date_done) from stock_picking where name=%s limit 1"
                self.env.cr.execute(get_date_done_date, ([pick_name]))
                abc = self.env.cr.fetchall()

                if len(abc)>0:
                    import pdb
                    pdb.set_trace()
                    update_query_2 = "update account_invoice set date_invoice=%s where id=%s"
                    self.env.cr.execute(update_query_2, (abc[0],inv_id))
                    self.env.cr.commit()

        active_ids = context.get('active_ids', []) or []

        for record in proxy.browse(self.env.cr, self.env.uid, inv_list, context=context):
            if record.state in ('open') and record.id not in [53,35,34,33,31,30,8,4]:
                record.signal_workflow('invoice_cancel')
                record.action_cancel_draft()
                record.signal_workflow('invoice_open')



        return True


    @api.multi
    def pos_stock_journal(self, context=None):
        # vals_parameter = [('create_date', '<=', '2022-02-25 07:53:42.652096')]
        vals_parameter = [('create_date', '>=', '2021-10-31 23:59:44.652096'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        # vals_parameter = [('create_date', '>=', '2021-08-10 23:59:42.652096'),('create_date', '<=', '2021-08-12 23:59:42.652096')]
        pos_order = self.env['pos.order.line'].search(vals_parameter)

        for stored_obj in pos_order:
            name = str(stored_obj.name)
            qty=stored_obj.qty
            if qty>0:
                standard_price=stored_obj.product_id.standard_price
                total_standard_price=standard_price*qty

                # product_id=stored_obj.inventory_product_entry_line_ids.product_name.id
                # product = self.env['product.product'].search([('id', '=', product_id)])
                # unit_amount = product.price_get('standard_price')[product.id]
                line_ids = []

                if context is None: context = {}
                if context.get('period_id', False):
                    return context.get('period_id')
                periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
                period_id = periods and periods[0] or False
                dates = stored_obj.create_date
                dt=datetime.strptime(dates, '%Y-%m-%d %H:%M:%S').date()
                if dt.month == 2:
                    period_id = 29
                if dt.month == 1:
                    period_id = 28
                if dt.month == 12:
                    period_id = 27
                if dt.month == 11:
                    period_id = 26
                if dt.month == 10:
                    period_id = 25
                if dt.month == 9:
                    period_id = 24
                if dt.month == 8:
                    period_id = 23
                if dt.month == 7:
                    period_id = 22
                if dt.month == 6:
                    period_id = 22


                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': name,
                    'currency_id': False,
                    'account_id': 274,
                    'credit': total_standard_price,
                    'date_maturity': False,
                    'debit': 0,
                    'amount_currency': 0,

                }))

                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': name,
                    'currency_id': False,
                    'account_id': 6325,
                    'credit': 0,
                    'date_maturity': False,
                    'debit': total_standard_price,
                    'amount_currency': 0,
                }))

                jv_entry = self.pool.get('account.move')

                j_vals = {'name': '/',
                          'journal_id': 1,  ## Sales Journal
                          'date': dt,
                          'period_id': period_id,
                          'ref': name,
                          'line_id': line_ids
                          }

                saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
                if saved_jv_id > 0:
                    journal_id = saved_jv_id
                    try:
                        jv_entry.button_validate(self.env.cr, self.env.uid, [saved_jv_id], context)
                    except:
                        import pdb
                        pdb.set_trace()


        return True
#optics journal
    @api.multi
    def optics_stock_journal(self, context=None):
        # vals_parameter = [('create_date', '<=', '2022-02-25 07:53:42.652096')]
        vals_parameter = [('create_date', '>=', '2021-07-12 07:53:43.652096'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        opt_order = self.env['optics.sale'].search(vals_parameter)

        for stored_obj in opt_order:
            name = str(stored_obj.name)
            frame_standard_price=0
            cover_price=0
            cellpad_price=0
            lens_price=0
            qty = stored_obj.quantity
            if qty>0:
                standard_price = stored_obj.frame_id.standard_price
                frame_standard_price = standard_price * qty
            if stored_obj.hard_cover is True:
                hard_cover_obj=self.env['product.template'].search([('id','=',187)])
                cover_price=hard_cover_obj.standard_price
            if stored_obj.cell_pad is True:
                cell_pad_obj=self.env['product.template'].search([('id','=',188)])
                cellpad_price = cell_pad_obj.standard_price
            if stored_obj.optics_lens_sale_line_id.name.name:
                lens_obj = self.env['product.template'].search([('id', '=', 190)])
                lens_price=lens_obj.standard_price
            total_standard_price=frame_standard_price+cover_price+cellpad_price+lens_price



            # product_id=stored_obj.inventory_product_entry_line_ids.product_name.id
            # product = self.env['product.product'].search([('id', '=', product_id)])
            # unit_amount = product.price_get('standard_price')[product.id]
            line_ids = []

            if context is None: context = {}
            if context.get('period_id', False):
                return context.get('period_id')
            periods = self.pool.get('account.period').find(self.env.cr, self.env.uid, context=context)
            period_id = periods and periods[0] or False
            dates = stored_obj.create_date
            dt = datetime.strptime(dates, '%Y-%m-%d %H:%M:%S').date()
            if dt.month == 2:
                period_id = 29
            if dt.month == 1:
                period_id = 28
            if dt.month == 12:
                period_id = 27
            if dt.month == 11:
                period_id = 26
            if dt.month == 10:
                period_id = 25
            if dt.month == 9:
                period_id = 24
            if dt.month == 8:
                period_id = 23
            if dt.month == 7:
                period_id = 22
            if dt.month == 6:
                period_id = 22

            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': name,
                'currency_id': False,
                'account_id': 278, #stock of specticle goods
                'credit': total_standard_price,
                'date_maturity': False,
                'debit': 0,
                'amount_currency': 0,

            }))

            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': name,
                'currency_id': False,
                'account_id': 135, #cost of specticles
                'credit': 0,
                'date_maturity': False,
                'debit': total_standard_price,
                'amount_currency': 0,
            }))

            jv_entry = self.pool.get('account.move')

            j_vals = {'name': '/',
                      'journal_id': 1,  ## Sales Journal
                      'date': dt,
                      'period_id': period_id,
                      'ref': name,
                      'line_id': line_ids
                      }
            saved_jv_id = jv_entry.create(self.env.cr, self.env.uid, j_vals, context=context)
            if saved_jv_id > 0:
                journal_id = saved_jv_id
                try:
                    jv_entry.button_validate(self.env.cr, self.env.uid, [saved_jv_id], context)
                except:
                    import pdb
                    pdb.set_trace()

        return True

    # select
    # product_id, qty, name, create_date, price_subtotal
    # from pos_order_line where
    # create_date < '2022-02-25 00:00:00'



