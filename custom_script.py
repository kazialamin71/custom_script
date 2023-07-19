
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
    def check_billss(self, context=None):
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
                        "purchase_order.state in('approved','done') and purchase_order_line.product_id=%s " \
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

    @api.multi
    def check_bill(self, context=None):
        vals_parameter = [('create_date', '<=', '2022-02-25 07:53:42.652096')]
        mr_obj = self.env['optics.sale'].search(vals_parameter)
        bill_no = []
        for stored_obj in mr_obj:

            try:
                name=stored_obj.optics_lens_sale_line_id.name.name
            except:
                bill_no.append(stored_obj.name)



        return True

    @api.multi
    def optics_unlink_journal(self, context=None):

        res =[]
        dlt_list = [488328 ,488327 ,488326 ,488325 ,488324 ,488323 ,488322 ,488321 ,488320 ,488319 ,488318 ,488317 ,488316 ,488315 ,488314 ,488313 ,488312 ,488310 ,488309 ,488308 ,488307 ,488306 ,488305 ,488304 ,488303 ,488302 ,488301 ,488300 ,488299 ,488298 ,488297 ,488296 ,488295 ,488294 ,488293 ,488292 ,488291 ,488290 ,488289 ,488287 ,488286 ,488285 ,488284 ,488283 ,488282 ,488281 ,488280 ,488279 ,488278 ,488277 ,488276 ,488275 ,488274 ,488273 ,488271 ,488270 ,488269 ,488268 ,488267 ,488266 ,488265 ,488264 ,488263 ,488262 ,488261 ,488260 ,488259 ,488258 ,488257 ,488256 ,488255 ,488254 ,488253 ,488252 ,488251 ,488250 ,488249 ,488248 ,488247 ,488246 ,488245 ,488244 ,488243 ,488242 ,488241 ,488240 ,488239 ,488238 ,488237 ,488236 ,488235 ,488234 ,488233 ,488232 ,488231 ,488230 ,488229 ,488228 ,488227 ,488226 ,488225 ,488224 ,488223 ,488222 ,488221 ,488220 ,488219 ,488218 ,488217 ,488216 ,488215 ,488214 ,488213 ,488212 ,488211 ,488210 ,488209 ,488208 ,488207 ,488206 ,488205 ,488204 ,488203 ,488202 ,488201 ,488200 ,488198 ,488197 ,488196 ,488195 ,488194 ,488193 ,488192 ,488191 ,488190 ,488189 ,488188 ,488187 ,488186 ,488185 ,488184 ,488183 ,488182 ,488181 ,488180 ,488179 ,488178 ,488177 ,488176 ,488175 ,488174 ,488173 ,488172 ,488171 ,488170 ,488169 ,488168 ,488167 ,488166 ,488165 ,488164 ,488163 ,488162 ,488161 ,488160 ,488159 ,488158 ,488157 ,488156 ,488155 ,488154 ,488153 ,488152 ,488151 ,488150 ,488149 ,488148 ,488147 ,488145 ,488144 ,488143 ,488142 ,488141 ,488140 ,488139 ,488138 ,488137 ,488136 ,488135 ,488134 ,488133 ,488132 ,488131 ,488130 ,488129 ,488128 ,488127 ,488126 ,488125 ,488124 ,488123 ,488122 ,488121 ,488120 ,488119 ,488118 ,488117 ,488116 ,488115 ,488114 ,488113 ,488112 ,488111 ,488110 ,488109 ,488108 ,488107 ,488106 ,488105 ,488104 ,488103 ,488102 ,488101 ,488100 ,488099 ,488098 ,488097 ,488096 ,488095 ,488094 ,488093 ,488092 ,488091 ,488090 ,488089 ,488088 ,488087 ,488086 ,488085 ,488084 ,488083 ,488082 ,488081 ,488080 ,488079 ,488078 ,488077 ,488076 ,488075 ,488074 ,488073 ,488072 ,488071 ,488070 ,488069 ,488068 ,488067 ,488066 ,488065 ,488064 ,488063 ,488062 ,488061 ,488060 ,488059 ,488058 ,488057 ,488056 ,488055 ,488054 ,488053 ,488052 ,488051 ,488050 ,488049 ,488048 ,488047 ,488046 ,488045 ,488044 ,488043 ,488042 ,488041 ,488040 ,488039 ,488038 ,488037 ,488036 ,488035 ,488034 ,488033 ,488032 ,488031 ,488030 ,488028 ,488027 ,488026 ,488025 ,488024 ,488023 ,488022 ,488021 ,488020 ,488019 ,488018 ,488017 ,488016 ,488015 ,488014 ,488013 ,488012 ,488011 ,488010 ,488009 ,488008 ,488007 ,488006 ,488005 ,488004 ,488003 ,488002 ,488001 ,488000 ,487999 ,487998 ,487997 ,487996 ,487995 ,487994 ,487993 ,487992 ,487991 ,487990 ,487989 ,487988 ,487987 ,487986 ,487985 ,487984 ,487983 ,487982 ,487981 ,487980 ,487979 ,487978 ,487977 ,487976 ,487975 ,487974 ,487973 ,487972 ,487971 ,487970 ,487969 ,487968 ,487967 ,487966 ,487965 ,487964 ,487963 ,487962 ,487961 ,487960 ,487959 ,487958 ,487957 ,487956 ,487955 ,487954 ,487953 ,487952 ,487950 ,487949 ,487948 ,487947 ,487946 ,487945 ,487944 ,487943 ,487942 ,487941 ,487940 ,487939 ,487938 ,487936 ,487935 ,487934 ,487933 ,487932 ,487931 ,487930 ,487929 ,487928 ,487927 ,487926 ,487925 ,487924 ,487923 ,487922 ,487921 ,487920 ,487919 ,487918 ,487917 ,487916 ,487915 ,487914 ,487913 ,487912 ,487911 ,487910 ,487909 ,487908 ,487907 ,487906 ,487905 ,487904 ,487903 ,487901 ,487900 ,487899 ,487898 ,487897 ,487896 ,487895 ,487894 ,487893 ,487892 ,487891 ,487890 ,487889 ,487888 ,487887 ,487886 ,487885 ,487884 ,487883 ,487882 ,487881 ,487880 ,487879 ,487878 ,487877 ,487876 ,487875 ,487874 ,487873 ,487872 ,487871 ,487870 ,487869 ,487868 ,487867 ,487866 ,487865 ,487864 ,487863 ,487862 ,487861 ,487860 ,487859 ,487858 ,487857 ,487856 ,487855 ,487854 ,487853 ,487852 ,487851 ,487850 ,487849 ,487848 ,487846 ,487845 ,487844 ,487843 ,487842 ,487841 ,487840 ,487839 ,487838 ,487837 ,487836 ,487835 ,487834 ,487833 ,487832 ,487831 ,487830 ,487829 ,487828 ,487827 ,487826 ,487825 ,487824 ,487823 ,487822 ,487821 ,487820 ,487819 ,487818 ,487817 ,487816 ,487815 ,487814 ,487813 ,487812 ,487811 ,487810 ,487809 ,487808 ,487807 ,487806 ,487805 ,487804 ,487803 ,487802 ,487801 ,487800 ,487799 ,487798 ,487797 ,487796 ,487795 ,487794 ,487793 ,487792 ,487791 ,487790 ,487789 ,487788 ,487787 ,487786 ,487785 ,487784 ,487783 ,487782 ,487781 ,487780 ,487779 ,487778 ,487777 ,487776 ,487775 ,487774 ,487773 ,487772 ,487771 ,487770 ,487769 ,487768 ,487767 ,487766 ,487765 ,487764 ,487763 ,487762 ,487761 ,487760 ,487759 ,487758 ,487757 ,487756 ,487755 ,487754 ,487753 ,487752 ,487751 ,487750 ,487749 ,487748 ,487747 ,487746 ,487745 ,487744 ,487743 ,487742 ,487741 ,487740 ,487739 ,487738 ,487737 ,487736 ,487735 ,487734 ,487733 ,487732 ,487731 ,487730 ,487729 ,487728 ,487727 ,487726 ,487725 ,487724 ,487723 ,487722 ,487721 ,487720 ,487719 ,487718 ,487717 ,487716 ,487715 ,487714 ,487713 ,487712 ,487711 ,487710 ,487709 ,487708 ,487707 ,487706 ,487705 ,487704 ,487703 ,487702 ,487701 ,487700 ,487699 ,487698 ,487697 ,487696 ,487695 ,487694 ,487693 ,487692 ,487691 ,487690 ,487689 ,487688 ,487687 ,487686 ,487685 ,487684 ,487683 ,487682 ,487681 ,487680 ,487679 ,487678 ,487677 ,487676 ,487675 ,487674 ,487673 ,487672 ,487671 ,487670 ,487669 ,487668 ,487667 ,487666 ,487665 ,487664 ,487663 ,487661 ,487659 ,487657 ,487655 ,487653 ,487652 ,487651 ,487650 ,487649 ,487648 ,487647 ,487646 ,487645 ,487644 ,487643 ,487642 ,487641 ,487640 ,487639 ,487638 ,487637 ,487636 ,487635 ,487634 ,487633 ,487632 ,487631 ,487630 ,487629 ,487628 ,487627 ,487626 ,487625 ,487624 ,487623 ,487622 ,487621 ,487620 ,487619 ,487618 ,487617 ,487616 ,487615 ,487614 ,487613 ,487612 ,487611 ,487610 ,487609 ,487608 ,487607 ,487606 ,487605 ,487604 ,487603 ,487602 ,487601 ,487600 ,487599 ,487598 ,487597 ,487596 ,487595 ,487594 ,487593 ,487592 ,487591 ,487590 ,487589 ,487588 ,487587 ,487586 ,487585 ,487584 ,487583 ,487582 ,487581 ,487580 ,487579 ,487578 ,487577 ,487576 ,487575 ,487574 ,487573 ,487572 ,487571 ,487570 ,487569 ,487568 ,487567 ,487566 ,487565 ,487564 ,487563 ,487562 ,487561 ,487560 ,487559 ,487558 ,487557 ,487556 ,487554 ,487553 ,487552 ,487551 ,487550 ,487549 ,487548 ,487547 ,487546 ,487545 ,487544 ,487543 ,487542 ,487541 ,487540 ,487539 ,487538 ,487537 ,487536 ,487534 ,487532 ,487531 ,487529 ,487527 ,487525 ,487524 ,487523 ,487522 ,487521 ,487520 ,487519 ,487518 ,487517 ,487516 ,487515 ,487514 ,487513 ,487512 ,487511 ,487510 ,487509 ,487508 ,487507 ,487506 ,487505 ,487504 ,487503 ,487502 ,487501 ,487500 ,487499 ,487498 ,487497 ,487496 ,487495 ,487494 ,487493 ,487492 ,487491 ,487490 ,487489 ,487488 ,487487 ,487486 ,487485 ,487484 ,487483 ,487482 ,487481 ,487480 ,487479 ,487478 ,487477 ,487476 ,487475 ,487474 ,487473 ,487472 ,487471 ,487470 ,487469 ,487468 ,487467 ,487466 ,487465 ,487464 ,487463 ,487462 ,487461 ,487460 ,487459 ,487458 ,487457 ,487456 ,487455 ,487454 ,487453 ,487452 ,487451 ,487450 ,487449 ,487448 ,487446 ,487445 ,487444 ,487443 ,487442 ,487441 ,487440 ,487439 ,487438 ,487437 ,487436 ,487435 ,487434 ,487433 ,487432 ,487431 ,487430 ,487429 ,487428 ,487427 ,487426 ,487425 ,487424 ,487423 ,487422 ,487421 ,487420 ,487419 ,487418 ,487417 ,487416 ,487415 ,487414 ,487413 ,487412 ,487411 ,487410 ,487409 ,487408 ,487407 ,487406 ,487405 ,487404 ,487403 ,487402 ,487401 ,487400 ,487399 ,487398 ,487397 ,487396 ,487395 ,487394 ,487393 ,487392 ,487391 ,487390 ,487389 ,487388 ,487387 ,487386 ,487385 ,487384 ,487383 ,487382 ,487381 ,487380 ,487379 ,487378 ,487377 ,487376 ,487375 ,487374 ,487373 ,487372 ,487371 ,487370 ,487369 ,487368 ,487367 ,487366 ,487365 ,487364 ,487363 ,487362 ,487361 ,487360 ,487359 ,487358 ,487357 ,487356 ,487355 ,487354 ,487353 ,487352 ,487351 ,487350 ,487349 ,487348 ,487347 ,487346 ,487345 ,487344 ,487343 ,487342 ,487341 ,487340 ,487339 ,487337 ,487335 ,487334 ,487333 ,487332 ,487331 ,487330 ,487329 ,487328 ,487327 ,487326 ,487325 ,487324 ,487323 ,487322 ,487321 ,487320 ,487319 ,487317 ,487316 ,487315 ,487314 ,487313 ,487312 ,487311 ,487310 ,487309 ,487308 ,487307 ,487306 ,487305 ,487304 ,487303 ,487302 ,487301 ,487300 ,487298 ,487296 ,487294 ,487292 ,487291 ,487289 ,487288 ,487287 ,487286 ,487285 ,487284 ,487283 ,487282 ,487281 ,487280 ,487279 ,487278 ,487277 ,487276 ,487275 ,487274 ,487273 ,487272 ,487271 ,487270 ,487269 ,487268 ,487267 ,487266 ,487265 ,487264 ,487263 ,487262 ,487261 ,487260 ,487259 ,487258 ,487257 ,487256 ,487255 ,487254 ,487253 ,487252 ,487251 ,487250 ,487249 ,487248 ,487247 ,487246 ,487245 ,487244 ,487243 ,487242 ,487241 ,487240 ,487239 ,487238 ,487237 ,487236 ,487235 ,487234 ,487233 ,487232 ,487231 ,487230 ,487229 ,487228 ,487227 ,487226 ,487225 ,487224 ,487223 ,487222 ,487221 ,487220 ,487219 ,487218 ,487217 ,487216 ,487215 ,487214 ,487213 ,487212 ,487211 ,487210 ,487209 ,487208 ,487207 ,487206 ,487205 ,487204 ,487203 ,487202 ,487201 ,487200 ,487199 ,487198 ,487197 ,487196 ,487195 ,487194 ,487193 ,487192 ,487191 ,487190 ,487189 ,487188 ,487187 ,487186 ,487185 ,487184 ,487183 ,487182 ,487181 ,487180 ,487179 ,487178 ,487177 ,487176 ,487175 ,487173 ,487171 ,487169 ,487168 ,487166 ,487164 ,487163 ,487162 ,487161 ,487160 ,487159 ,487158 ,487157 ,487156 ,487155 ,487154 ,487153 ,487152 ,487151 ,487150 ,487149 ,487148 ,487147 ,487146 ,487145 ,487144 ,487143 ,487142 ,487141 ,487140 ,487139 ,487138 ,487137 ,487136 ,487135 ,487134 ,487133 ,487132 ,487131 ,487130 ,487129 ,487128 ,487127 ,487126 ,487125 ,487124 ,487123 ,487122 ,487121 ,487120 ,487119 ,487118 ,487117 ,487116 ,487115 ,487114 ,487113 ,487112 ,487111 ,487110 ,487109 ,487107 ,487105 ,487103 ,487101 ,487099 ,487098 ,487097 ,487096 ,487095 ,487094 ,487093 ,487092 ,487091 ,487090 ,487089 ,487088 ,487087 ,487086 ,487085 ,487084 ,487083 ,487082 ,487080 ,487078 ,487076 ,487074 ,487073 ,487071 ,487070 ,487069 ,487068 ,487067 ,487066 ,487065 ,487064 ,487063 ,487062 ,487061 ,487060 ,487059 ,487058 ,487057 ,487056 ,487055 ,487054 ,487053 ,487052 ,487051 ,487050 ,487049 ,487048 ,487047 ,487046 ,487045 ,487044 ,487043 ,487042 ,487041 ,487040 ,487038 ,487037 ,487036 ,487035 ,487033 ,487032 ,487031 ,487030 ,487029 ,487028 ,487027 ,487026 ,487025 ,487024 ,487023 ,487022 ,487021 ,487020 ,487019 ,487018 ,487017 ,487016 ,487015 ,487014 ,487013 ,487012 ,487011 ,487010 ,487009 ,487008 ,487007 ,487006 ,487005 ,487004 ,487003 ,487002 ,487001 ,487000 ,486999 ,486997 ,486996 ,486995 ,486994 ,486993 ,486992 ,486991 ,486990 ,486989 ,486988 ,486987 ,486986 ,486985 ,486984 ,486983 ,486982 ,486981 ,486980 ,486979 ,486978 ,486977 ,486976 ,486975 ,486974 ,486973 ,486972 ,486971 ,486970 ,486969 ,486968 ,486967 ,486966 ,486964 ,486963 ,486962 ,486961 ,486960 ,486959 ,486958 ,486957 ,486956 ,486955 ,486954 ,486953 ,486952 ,486951 ,486950 ,486949 ,486948 ,486947 ,486946 ,486945 ,486944 ,486942 ,486941 ,486940 ,486939 ,486938 ,486937 ,486936 ,486935 ,486934 ,486933 ,486931 ,486930 ,486929 ,486928 ,486927 ,486926 ,486925 ,486924 ,486923 ,486922 ,486921 ,486920 ,486919 ,486918 ,486917 ,486916 ,486915 ,486914 ,486913 ,486912 ,486911 ,486910 ,486909 ,486908 ,486907 ,486906 ,486905 ,486904 ,486903 ,486902 ,486901 ,486900 ,486899 ,486898 ,486897 ,486896 ,486895 ,486894 ,486893 ,486892 ,486891 ,486890 ,486889 ,486888 ,486887 ,486886 ,486885 ,486884 ,486883 ,486882 ,486881 ,486880 ,486879 ,486878 ,486877 ,486876 ,486875 ,486874 ,486873 ,486872 ,486871 ,486870 ,486869 ,486868 ,486867 ,486866 ,486865 ,486864 ,486863 ,486862 ,486861 ,486860 ,486859 ,486858 ,486857 ,486856 ,486855 ,486854 ,486853 ,486851 ,486850 ,486849 ,486848 ,486847 ,486846 ,486845 ,486844 ,486843 ,486841 ,486840 ,486839 ,486838 ,486837 ,486835 ,486834 ,486833 ,486832 ,486831 ,486830 ,486829 ,486828 ,486827 ,486826 ,486825 ,486824 ,486823 ,486822 ,486821 ,486820 ,486819 ,486818 ,486817 ,486816 ,486815 ,486814 ,486813 ,486812 ,486811 ,486810 ,486809 ,486808 ,486807 ,486806 ,486805 ,486804 ,486803 ,486802 ,486801 ,486800 ,486799 ,486798 ,486797 ,486796 ,486795 ,486794 ,486793 ,486792 ,486791 ,486790 ,486789 ,486788 ,486787 ,486786 ,486785 ,486784 ,486783 ,486782 ,486781 ,486780 ,486779 ,486778 ,486777 ,486776 ,486775 ,486774 ,486773 ,486772 ,486771 ,486770 ,486769 ,486768 ,486767 ,486766 ,486765 ,486764 ,486763 ,486762 ,486761 ,486760 ,486759 ,486758 ,486757 ,486756 ,486755 ,486754 ,486753 ,486751 ,486750 ,486749 ,486748 ,486747 ,486746 ,486745 ,486744 ,486743 ,486742 ,486741 ,486740 ,486739 ,486738 ,486737 ,486736 ,486735 ,486734 ,486733 ,486732 ,486731 ,486730 ,486729 ,486728 ,486727 ,486726 ,486725 ,486724 ,486723 ,486722 ,486721 ,486720 ,486719 ,486718 ,486717 ,486716 ,486715 ,486714 ,486713 ,486712 ,486711 ,486710 ,486709 ,486708 ,486707 ,486706 ,486705 ,486704 ,486703 ,486702 ,486701 ,486700 ,486699 ,486698 ,486697 ,486696 ,486695 ,486694 ,486693 ,486692 ,486691 ,486690 ,486689 ,486688 ,486687 ,486686 ,486685 ,486684 ,486683 ,486682 ,486681 ,486680 ,486679 ,486678 ,486677 ,486676 ,486675 ,486674 ,486673 ,486672 ,486671 ,486670 ,486669 ,486668 ,486667 ,486666 ,486665 ,486664 ,486663 ,486662 ,486661 ,486660 ,486659 ,486658 ,486657 ,486656 ,486654 ,486652 ,486650 ,486649 ,486648 ,486647 ,486646 ,486645 ,486644 ,486643 ,486642 ,486641 ,486640 ,486639 ,486638 ,486637 ,486636 ,486635 ,486634 ,486633 ,486632 ,486631 ,486630 ,486629 ,486628 ,486627 ,486626 ,486625 ,486624 ,486623 ,486622 ,486621 ,486620 ,486619 ,486618 ,486617 ,486616 ,486615 ,486614 ,486613 ,486612 ,486610 ,486609 ,486608 ,486607 ,486606 ,486605 ,486604 ,486603 ,486602 ,486601 ,486600 ,486599 ,486598 ,486597 ,486596 ,486595 ,486594 ,486593 ,486592 ,486591 ,486590 ,486589 ,486588 ,486587 ,486586 ,486585 ,486584 ,486583 ,486582 ,486581 ,486580 ,486579 ,486578 ,486577 ,486576 ,486575 ,486574 ,486573 ,486572 ,486571 ,486570 ,486569 ,486568 ,486567 ,486566 ,486565 ,486564 ,486563 ,486562 ,486561 ,486560 ,486559 ,486558 ,486557 ,486556 ,486555 ,486554 ,486553 ,486552 ,486551 ,486550 ,486549 ,486548 ,486547 ,486546 ,486545 ,486544 ,486543 ,486542 ,486541 ,486540 ,486539 ,486538 ,486537 ,486536 ,486535 ,486534 ,486533 ,486532 ,486531 ,486530 ,486529 ,486528 ,486527 ,486526 ,486525 ,486524 ,486523 ,486522 ,486521 ,486520 ,486519 ,486518 ,486517 ,486516 ,486514 ,486513 ,486512 ,486511 ,486510 ,486509 ,486508 ,486507 ,486506 ,486505 ,486504 ,486503 ,486502 ,486501 ,486500 ,486499 ,486498 ,486497 ,486496 ,486495 ,486494 ,486493 ,486492 ,486491 ,486490 ,486489 ,486487 ,486486 ,486485 ,486484 ,486483 ,486482 ,486481 ,486480 ,486479 ,486478 ,486477 ,486476 ,486475 ,486474 ,486473 ,486472 ,486471 ,486470 ,486469 ,486468 ,486467 ,486466 ,486465 ,486464 ,486463 ,486462 ,486461 ,486460 ,486459 ,486458 ,486457 ,486456 ,486455 ,486454 ,486453 ,486452 ,486451 ,486450 ,486449 ,486448 ,486447 ,486446 ,486445 ,486444 ,486443 ,486442 ,486440 ,486438 ,486436 ,486433 ,486431 ,486430 ,486429 ,486428 ,486427 ,486426 ,486425 ,486424 ,486423 ,486422 ,486421 ,486420 ,486419 ,486418 ,486417 ,486416 ,486415 ,486414 ,486413 ,486412 ,486411 ,486410 ,486409 ,486408 ,486407 ,486406 ,486405 ,486404 ,486403 ,486402 ,486401 ,486400 ,486399 ,486398 ,486397 ,486396 ,486395 ,486394 ,486393 ,486392 ,486391 ,486390 ,486389 ,486388 ,486387 ,486386 ,486385 ,486384 ,486383 ,486382 ,486381 ,486380 ,486379 ,486378 ,486377 ,486376 ,486375 ,486374 ,486373 ,486372 ,486371 ,486370 ,486369 ,486368 ,486367 ,486366 ,486365 ,486364 ,486363 ,486362 ,486361 ,486360 ,486359 ,486358 ,486357 ,486356 ,486355 ,486354 ,486353 ,486352 ,486351 ,486350 ,486349 ,486348 ,486347 ,486346 ,486345 ,486344 ,486343 ,486342 ,486341 ,486340 ,486339 ,486338 ,486337 ,486336 ,486335 ,486334 ,486333 ,486332 ,486331 ,486330 ,486329 ,486328 ,486327 ,486325 ,486324 ,486323 ,486322 ,486321 ,486320 ,486319 ,486318 ,486317 ,486316 ,486315 ,486314 ,486313 ,486312 ,486311 ,486310 ,486309 ,486308 ,486307 ,486306 ,486305 ,486304 ,486303 ,486302 ,486301 ,486300 ,486299 ,486298 ,486296 ,486295 ,486294 ,486293 ,486292 ,486291 ,486290 ,486289 ,486288 ,486287 ,486286 ,486285 ,486284 ,486283 ,486282 ,486281 ,486280 ,486279 ,486278 ,486277 ,486276 ,486275 ,486274 ,486273 ,486272 ,486271 ,486270 ,486269 ,486268 ,486267 ,486266 ,486265 ,486264 ,486263 ,486262 ,486261 ,486260 ,486259 ,486258 ,486257 ,486256 ,486255 ,486254 ,486253 ,486252 ,486251 ,486250 ,486249 ,486248 ,486247 ,486246 ,486245 ,486244 ,486243 ,486242 ,486241 ,486240 ,486239 ,486238 ,486237 ,486236 ,486235 ,486234 ,486233 ,486232 ,486231 ,486230 ,486229 ,486228 ,486227 ,486226 ,486225 ,486224 ,486223 ,486222 ,486221 ,486220 ,486219 ,486218 ,486217 ,486216 ,486215 ,486214 ,486213 ,486212 ,486211 ,486210 ,486209 ,486208 ,486207 ,486206 ,486205 ,486204 ,486203 ,486201 ,486200 ,486199 ,486198 ,486197 ,486196 ,486195 ,486194 ,486193 ,486192 ,486191 ,486190 ,486189 ,486188 ,486187 ,486186 ,486185 ,486184 ,486183 ,486182 ,486181 ,486180 ,486179 ,486178 ,486177 ,486176 ,486174 ,486173 ,486172 ,486171 ,486170 ,486169 ,486168 ,486167 ,486166 ,486165 ,486164 ,486163 ,486162 ,486161 ,486160 ,486159 ,486158 ,486157 ,486156 ,486155 ,486154 ,486153 ,486152 ,486151 ,486150 ,486149 ,486148 ,486147 ,486146 ,486145 ,486144 ,486143 ,486142 ,486141 ,486139 ,486137 ,486136 ,486135 ,486134 ,486133 ,486132 ,486131 ,486130 ,486129 ,486128 ,486127 ,486126 ,486125 ,486124 ,486123 ,486122 ,486121 ,486120 ,486119 ,486118 ,486117 ,486116 ,486115 ,486114 ,486113 ,486112 ,486111 ,486110 ,486108 ,486107 ,486106 ,486105 ,486104 ,486103 ,486102 ,486101 ,486100 ,486099 ,486098 ,486097 ,486096 ,486095 ,486094 ,486093 ,486092 ,486091 ,486090 ,486089 ,486088 ,486087 ,486086 ,486085 ,486084 ,486083 ,486082 ,486080 ,486079 ,486078 ,486077 ,486076 ,486075 ,486074 ,486073 ,486072 ,486071 ,486070 ,486069 ,486068 ,486067 ,486066 ,486065 ,486064 ,486063 ,486062 ,486061 ,486060 ,486059 ,486058 ,486057 ,486056 ,486055 ,486054 ,486053 ,486052 ,486051 ,486050 ,486049 ,486048 ,486047 ,486046 ,486045 ,486044 ,486043 ,486042 ,486041 ,486040 ,486039 ,486038 ,486037 ,486036 ,486035 ,486034 ,486033 ,486032 ,486031 ,486030 ,486029 ,486028 ,486027 ,486026 ,486025 ,486024 ,486023 ,486022 ,486021 ,486019 ,486018 ,486017 ,486016 ,486015 ,486014 ,486013 ,486012 ,486011 ,486010 ,486009 ,486008 ,486007 ,486006 ,486005 ,486004 ,486003 ,486002 ,486001 ,486000 ,485999 ,485998 ,485997 ,485996 ,485995 ,485994 ,485993 ,485992 ,485991 ,485990 ,485989 ,485988 ,485987 ,485986 ,485985 ,485984 ,485983 ,485982 ,485981 ,485980 ,485979 ,485978 ,485977 ,485976 ,485975 ,485974 ,485973 ,485972 ,485971 ,485970 ,485969 ,485968 ,485967 ,485966 ,485965 ,485964 ,485963 ,485962 ,485961 ,485960 ,485959 ,485958 ,485957 ,485956 ,485955 ,485954 ,485953 ,485952 ,485951 ,485950 ,485949 ,485948 ,485947 ,485946 ,485945 ,485944 ,485943 ,485942 ,485941 ,485940 ,485939 ,485938 ,485937 ,485936 ,485935 ,485934 ,485933 ,485932 ,485931 ,485930 ,485929 ,485928 ,485927 ,485926 ,485925 ,485924 ,485923 ,485922 ,485921 ,485920 ,485919 ,485918 ,485917 ,485916 ,485915 ,485914 ,485913 ,485912 ,485911 ,485910 ,485909 ,485908 ,485907 ,485906 ,485905 ,485904 ,485903 ,485902 ,485901 ,485900 ,485899 ,485898 ,485897 ,485896 ,485895 ,485894 ,485893 ,485892 ,485891 ,485890 ,485889 ,485888 ,485887 ,485886 ,485885 ,485884 ,485883 ,485882 ,485881 ,485880 ,485879 ,485878 ,485877 ,485876 ,485875 ,485874 ,485873 ,485872 ,485871 ,485870 ,485869 ,485868 ,485867 ,485866 ,485865 ,485864 ,485863 ,485862 ,485861 ,485860 ,485859 ,485858 ,485857 ,485856 ,485855 ,485854 ,485853 ,485852 ,485851 ,485850 ,485849 ,485848 ,485847 ,485846 ,485845 ,485844 ,485843 ,485842 ,485841 ,485840 ,485839 ,485838 ,485837 ,485836 ,485835 ,485834 ,485833 ,485832 ,485831 ,485830 ,485829 ,485828 ,485827 ,485826 ,485825 ,485824 ,485823 ,485822 ,485821 ,485820 ,485819 ,485818 ,485817 ,485816 ,485815 ,485814 ,485813 ,485812 ,485811 ,485810 ,485809 ,485808 ,485807 ,485806 ,485805 ,485804 ,485803 ,485802 ,485801 ,485800 ,485799 ,485798 ,485797 ,485796 ,485795 ,485794 ,485793 ,485792 ,485791 ,485790 ,485789 ,485788 ,485787 ,485786 ,485785 ,485784 ,485783 ,485782 ,485781 ,485780 ,485779 ,485778 ,485777 ,485776 ,485775 ,485774 ,485773 ,485772 ,485771 ,485770 ,485769 ,485768 ,485767 ,485766 ,485765 ,485764 ,485763 ,485762 ,485761 ,485760 ,485759 ,485758 ,485757 ,485756 ,485754 ,485753 ,485752 ,485751 ,485750 ,485749 ,485748 ,485747 ,485746 ,485745 ,485744 ,485743 ,485742 ,485741 ,485740 ,485739 ,485738 ,485737 ,485736 ,485735 ,485734 ,485733 ,485732 ,485731 ,485730 ,485729 ,485728 ,485727 ,485726 ,485725 ,485724 ,485723 ,485722 ,485721 ,485720 ,485719 ,485718 ,485717 ,485716 ,485715 ,485714 ,485713 ,485712 ,485711 ,485710 ,485709 ,485708 ,485707 ,485706 ,485705 ,485704 ,485703 ,485702 ,485701 ,485700 ,485699 ,485698 ,485697 ,485696 ,485695 ,485694 ,485693 ,485692 ,485691 ,485690 ,485689 ,485688 ,485687 ,485686 ,485685 ,485684 ,485683 ,485682 ,485681 ,485680 ,485679 ,485678 ,485677 ,485676 ,485675 ,485674 ,485673 ,485672 ,485671 ,485670 ,485669 ,485668 ,485667 ,485666 ,485665 ,485664 ,485663 ,485662 ,485661 ,485660 ,485659 ,485658 ,485657 ,485656 ,485655 ,485654 ,485653 ,485652 ,485651 ,485650 ,485649 ,485648 ,485647 ,485646 ,485645 ,485644 ,485643 ,485642 ,485641 ,485640 ,485639 ,485638 ,485637 ,485636 ,485635 ,485634 ,485633 ,485632 ,485631 ,485630 ,485629 ,485628 ,485627 ,485626 ,485625 ,485624 ,485623 ,485622 ,485621 ,485620 ,485619 ,485618 ,485617 ,485616 ,485615 ,485614 ,485613 ,485612 ,485611 ,485610 ,485609 ,485608 ,485607 ,485606 ,485605 ,485604 ,485603 ,485602 ,485601 ,485600 ,485599 ,485598 ,485597 ,485596 ,485595 ,485594 ,485593 ,485592 ,485591 ,485590 ,485589 ,485588 ,485587 ,485586 ,485585 ,485583 ,485582 ,485581 ,485580 ,485579 ,485578 ,485577 ,485576 ,485575 ,485574 ,485573 ,485572 ,485571 ,485570 ,485569 ,485568 ,485567 ,485566 ,485565 ,485564 ,485563 ,485562 ,485561 ,485560 ,485559 ,485558 ,485557 ,485556 ,485555 ,485554 ,485553 ,485552 ,485551 ,485550 ,485549 ,485548 ,485547 ,485546 ,485545 ,485544 ,485543 ,485542 ,485541 ,485540 ,485539 ,485538 ,485537 ,485536 ,485535 ,485534 ,485533 ,485532 ,485531 ,485530 ,485529 ,485528 ,485527 ,485526 ,485525 ,485524 ,485523 ,485522 ,485521 ,485520 ,485519 ,485518 ,485517 ,485516 ,485515 ,485514 ,485513 ,485512 ,485511 ,485510 ,485509 ,485508 ,485507 ,485506 ,485505 ,485504 ,485503 ,485502 ,485501 ,485500 ,485499 ,485498 ,485497 ,485496 ,485495 ,485494 ,485493 ,485492 ,485491 ,485490 ,485489 ,485488 ,485487 ,485486 ,485485 ,485484 ,485483 ,485482 ,485481 ,485480 ,485479 ,485478 ,485477 ,485476 ,485475 ,485474 ,485473 ,485472 ,485471 ,485470 ,485469 ,485468 ,485467 ,485466 ,485465 ,485464 ,485463 ,485462 ,485461 ,485460 ,485459 ,485458 ,485457 ,485456 ,485455 ,485454 ,485453 ,485452 ,485451 ,485450 ,485449 ,485448 ,485447 ,485446 ,485444 ,485443 ,485442 ,485441 ,485440 ,485439 ,485438 ,485437 ,485436 ,485435 ,485434 ,485433 ,485432 ,485431 ,485430 ,485429 ,485428 ,485427 ,485426 ,485425 ,485424 ,485423 ,485422 ,485421 ,485420 ,485419 ,485418 ,485417 ,485416 ,485415 ,485414 ,485413 ,485412 ,485411 ,485410 ,485409 ,485408 ,485407 ,485406 ,485405 ,485404 ,485403 ,485402 ,485401 ,485400 ,485399 ,485398 ,485397 ,485396 ,485395 ,485394 ,485393 ,485392 ,485391 ,485390 ,485389 ,485388 ,485387 ,485386 ,485385 ,485384 ,485383 ,485382 ,485381 ,485380 ,485378 ,485377 ,485376 ,485375 ,485374 ,485373 ,485372 ,485371 ,485370 ,485369 ,485368 ,485367 ,485366 ,485365 ,485364 ,485363 ,485362 ,485361 ,485360 ,485359 ,485358 ,485357 ,485356 ,485355 ,485354 ,485353 ,485352 ,485351 ,485350 ,485349 ,485348 ,485347 ,485346 ,485345 ,485344 ,485343 ,485342 ,485341 ,485340 ,485339 ,485338 ,485337 ,485336 ,485335 ,485334 ,485333 ,485332 ,485331 ,485330 ,485329 ,485328 ,485327 ,485326 ,485325 ,485324 ,485323 ,485322 ,485321 ,485320 ,485319 ,485318 ,485317 ,485316 ,485315 ,485314 ,485313 ,485312 ,485311 ,485310 ,485309 ,485308 ,485307 ,485306 ,485305 ,485304 ,485303 ,485302 ,485301 ,485300 ,485299 ,485298 ,485297 ,485296 ,485295 ,485294 ,485293 ,485292 ,485291 ,485290 ,485289 ,485288 ,485287 ,485286 ,485285 ,485284 ,485283 ,485282 ,485281 ,485280 ,485279 ,485278 ,485277 ,485276 ,485275 ,485274 ,485273 ,485272 ,485271 ,485270 ,485269 ,485268 ,485267 ,485266 ,485265 ,485264 ,485263 ,485262 ,485261 ,485260 ,485259 ,485258 ,485257 ,485256 ,485255 ,485254 ,485253 ,485252 ,485251 ,485250 ,485249 ,485248 ,485247 ,485246 ,485245 ,485244 ,485242 ,485241 ,485240 ,485239 ,485238 ,485237 ,485236 ,485235 ,485234 ,485233 ,485232 ,485231 ,485230 ,485229 ,485228 ,485227 ,485226 ,485225 ,485224 ,485223 ,485222 ,485221 ,485220 ,485219 ,485218 ,485217 ,485216 ,485215 ,485214 ,485213 ,485212 ,485211 ,485210 ,485209 ,485208 ,485207 ,485206 ,485205 ,485204 ,485203 ,485202 ,485201 ,485200 ,485199 ,485198 ,485197 ,485196 ,485195 ,485194 ,485193 ,485192 ,485191 ,485190 ,485189 ,485188 ,485187 ,485186 ,485185 ,485184 ,485183 ,485182 ,485181 ,485180 ,485179 ,485178 ,485177 ,485176 ,485175 ,485173 ,485172 ,485171 ,485170 ,485169 ,485168 ,485167 ,485166 ,485165 ,485164 ,485163 ,485162 ,485161 ,485160 ,485159 ,485158 ,485157 ,485156 ,485155 ,485154 ,485153 ,485152 ,485151 ,485150 ,485149 ,485148 ,485147 ,485146 ,485145 ,485144 ,485143 ,485142 ,485141 ,485140 ,485139 ,485138 ,485137 ,485136 ,485135 ,485134 ,485133 ,485132 ,485131 ,485130 ,485129 ,485128 ,485127 ,485126 ,485125 ,485124 ,485123 ,485122 ,485121 ,485120 ,485119 ,485118 ,485117 ,485116 ,485115 ,485114 ,485113 ,485112 ,485111 ,485110 ,485109 ,485108 ,485107 ,485106 ,485105 ,485104 ,485103 ,485102 ,485101 ,485100 ,485099 ,485098 ,485097 ,485096 ,485095 ,485094 ,485093 ,485092 ,485091 ,485090 ,485089 ,485088 ,485087 ,485086 ,485085 ,485084 ,485083 ,485082 ,485081 ,485080 ,485079 ,485078 ,485077 ,485076 ,485075 ,485074 ,485073 ,485072 ,485071 ,485070 ,485069 ,485067 ,485066 ,485065 ,485064 ,485063 ,485062 ,485061 ,485059 ,485058 ,485057 ,485056 ,485055 ,485054 ,485053 ,485052 ,485051 ,485050 ,485049 ,485048 ,485047 ,485046 ,485045 ,485044 ,485043 ,485042 ,485041 ,485040 ,485039 ,485038 ,485037 ,485036 ,485035 ,485034 ,485033 ,485032 ,485031 ,485030 ,485029 ,485028 ,485027 ,485026 ,485025 ,485024 ,485023 ,485022 ,485021 ,485020 ,485019 ,485018 ,485017 ,485016 ,485015 ,485014 ,485013 ,485012 ,485011 ,485010 ,485009 ,485008 ,485007 ,485006 ,485005 ,485004 ,485003 ,485002 ,485001 ,485000 ,484999 ,484998 ,484997 ,484996 ,484994 ,484993 ,484992 ,484991 ,484990 ,484989 ,484988 ,484987 ,484985 ,484984 ,484983 ,484982 ,484981 ,484980 ,484979 ,484978 ,484977 ,484976 ,484975 ,484974 ,484973 ,484972 ,484971 ,484970 ,484969 ,484968 ,484967 ,484966 ,484965 ,484964 ,484963 ,484962 ,484961 ,484960 ,484959 ,484958 ,484957 ,484956 ,484955 ,484954 ,484953 ,484952 ,484951 ,484950 ,484949 ,484948 ,484947 ,484946 ,484945 ,484944 ,484943 ,484942 ,484941 ,484940 ,484939 ,484938 ,484937 ,484936 ,484935 ,484934 ,484933 ,484932 ,484931 ,484930 ,484929 ,484928 ,484927 ,484926 ,484925 ,484924 ,484923 ,484922 ,484921 ,484920 ,484919 ,484918 ,484917 ,484916 ,484915 ,484914 ,484913 ,484912 ,484911 ,484910 ,484909 ,484908 ,484907 ,484906 ,484905 ,484904 ,484903 ,484902 ,484901 ,484900 ,484899 ,484898 ,484897 ,484896 ,484895 ,484894 ,484893 ,484892 ,484891 ,484890 ,484889 ,484888 ,484887 ,484886 ,484885 ,484884 ,484883 ,484882 ,484881 ,484880 ,484879 ,484878 ,484877 ,484876 ,484875 ,484874 ,484873 ,484872 ,484871 ,484870 ,484869 ,484868 ,484867 ,484866 ,484865 ,484864 ,484863 ,484862 ,484861 ,484860 ,484859 ,484858 ,484857 ,484856 ,484855 ,484854 ,484853 ,484852 ,484851 ,484850 ,484849 ,484848 ,484847 ,484846 ,484845 ,484844 ,484843 ,484842 ,484841 ,484840 ,484839 ,484838 ,484837 ,484836 ,484835 ,484834 ,484833 ,484832 ,484831 ,484830 ,484829 ,484828 ,484827 ,484826 ,484825 ,484824 ,484823 ,484822 ,484821 ,484820 ,484819 ,484818 ,484817 ,484816 ,484815 ,484814 ,484813 ,484812 ,484811 ,484810 ,484809 ,484808 ,484807 ,484806 ,484805 ,484804 ,484803 ,484802 ,484801 ,484800 ,484799 ,484798 ,484797 ,484796 ,484795 ,484794 ,484793 ,484792 ,484791 ,484790 ,484789 ,484788 ,484787 ,484786 ,484785 ,484784 ,484783 ,484782 ,484781 ,484780 ,484779 ,484778 ,484777 ,484776 ,484775 ,484773 ,484772 ,484771 ,484770 ,484769 ,484768 ,484767 ,484766 ,484765 ,484764 ,484763 ,484762 ,484761 ,484760 ,484759 ,484758 ,484757 ,484756 ,484755 ,484754 ,484753 ,484752 ,484751 ,484750 ,484749 ,484748 ,484747 ,484746 ,484745 ,484744 ,484743 ,484742 ,484741 ,484740 ,484739 ,484738 ,484737 ,484736 ,484735 ,484734 ,484733 ,484732 ,484731 ,484730 ,484729 ,484728 ,484727 ,484726 ,484725 ,484724 ,484723 ,484722 ,484721 ,484720 ,484719 ,484718 ,484717 ,484716 ,484715 ,484714 ,484713 ,484712 ,484711 ,484710 ,484709 ,484708 ,484707 ,484706 ,484705 ,484704 ,484703 ,484702 ,484701 ,484700 ,484699 ,484698 ,484697 ,484696 ,484695 ,484694 ,484693 ,484692 ,484691 ,484690 ,484689 ,484688 ,484687 ,484686 ,484685 ,484684 ,484683 ,484682 ,484681 ,484680 ,484679 ,484678 ,484677 ,484676 ,484675 ,484674 ,484673 ,484672 ,484671 ,484670 ,484669 ,484668 ,484667 ,484666 ,484665 ,484664 ,484663 ,484662 ,484661 ,484660 ,484659 ,484658 ,484657 ,484656 ,484654 ,484653 ,484652 ,484651 ,484650 ,484649 ,484648 ,484647 ,484646 ,484645 ,484644 ,484643 ,484642 ,484641 ,484640 ,484639 ,484638 ,484637 ,484636 ,484635 ,484634 ,484633 ,484632 ,484631 ,484630 ,484629 ,484628 ,484627 ,484626 ,484625 ,484624 ,484623 ,484622 ,484621 ,484620 ,484619 ,484618 ,484617 ,484616 ,484614 ,484613 ,484612 ,484610]

        move_pool = self.pool.get('account.move')
        move_pool.button_cancel(self.env.cr, self.env.uid, dlt_list, context=context)
        move_pool.unlink(self.env.cr, self.env.uid, dlt_list, context=context)
        # move_pool.button_validate(self.env.cr, self.env.uid, dlt_list, context=context)


        return res



