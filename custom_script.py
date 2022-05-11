
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
        vals_parameter = [('state', '=', 'activated'),('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
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
        # ### Custom Funcition
        vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
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
        vals_parameter = [('state', '=', 'confirmed'), ('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
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
            import pdb
            pdb.set_trace()
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
        vals_parameter = [('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]
        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['opd.ticket'].search(vals_parameter)
        for stored_obj in mr_obj:
            line_ids = []

            if context is None: context = {}
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
        # vals_parameter = [('state', '=', 'confirmed'),('create_date', '>=', '2021-07-01 04:46:56.269666'), ('create_date', '<=', '2021-07-31 13:18:37.700759')]
        vals_parameter = [('state', '=', 'activated'), ('create_date', '>=', '2021-09-30 13:18:38.048066'),('create_date', '<=', '2022-02-25 07:53:42.652096')]

        # vals_parameter.append(('date', '=', self.date))
        mr_obj = self.env['leih.admission'].search(vals_parameter)
        # import pdb
        # pdb.set_trace()
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

        vals_parameter = [('date_invoice', '<=', '2022-02-25 07:53:42.652096'), ('type', '=', 'in_invoice'),('state','=','open')]
        inv_obj = self.env['account.invoice'].search(vals_parameter)

        update_list = []

        inv_list = []


        for itms in inv_obj:

            inv_list.append(itms.id)

            for line_itm in itms.invoice_line:
                update_list.append((line_itm.product_id.categ_id.property_stock_valuation_account_id.id,line_itm.id))


        for list_itms in update_list:
            update_query = "update account_invoice_line set account_id=%s where id=%s"
            self.env.cr.execute(update_query,list_itms)
            self.env.cr.commit()


        proxy = self.pool['account.invoice']
        active_ids = context.get('active_ids', []) or []

        for record in proxy.browse(self.env.cr, self.env.uid, inv_list, context=context):
            if record.state in ('open'):
                record.signal_workflow('invoice_cancel')
                record.action_cancel_draft()
                record.signal_workflow('invoice_open')



        return True



