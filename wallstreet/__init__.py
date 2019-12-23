def get_index_for_dude(dude):
    """

    :param dude: splitwise user object
    :return: index in row/column in payment matrix for the incoming dude
    """
    if dude.first_name == "Alex":
        return 0
    elif dude.first_name == "Daniel":
        return 1
    elif dude.first_name == "Patrick":
        return 2
    elif dude.first_name == "maany":
        return 3


def payment_matrix(expenses):
    """
    Generate a raw payment matrix
              alex danny maany patrick
            ___________________________
    alex    |
    danny   |
    maany   |
    patrick |

    :param expenses: group expenses from splitwise api
    :return:
    """
    matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    for expense in expenses:
        paid_by = [ x for x in expense.users if float(x.net_balance) > 0]
        owed_by = [ x for x in expense.users if float(x.net_balance) < 0]
        if len(paid_by) > 1:
            raise RuntimeError("Complex payment. Multiple people paid. Cannot process in the patrix right now")
        if int(paid_by[0].id) in [int(user.id) for user in owed_by]:
            print("Same person paid and owes?")
        print("Expense: {expense}".format(expense=expense.description))
        print("Paid By: {paid_by}".format(paid_by=paid_by[0].first_name))
        print("Amount: {amount}".format(amount=paid_by[0].net_balance))
        print("Dudes who owe: {dude_who_owe}".format(dude_who_owe=[user.first_name for user in owed_by]))

        for dude_who_owes in owed_by:
            x = get_index_for_dude(paid_by[0])
            y = get_index_for_dude(dude_who_owes)
            amount = -1 * float(dude_who_owes.net_balance)
            print("{dude} need to pay {amount}. Updating X: {x}, Y: {y}".format(dude=dude_who_owes.first_name,
                                                                                amount =dude_who_owes.net_balance,
                                                                                x = x,
                                                                                y = y))
            matrix[x][y] = amount
    return matrix


def simplify_matrix(matrix):
    """
    If A owes B and B owes A back, then only a single transaction can settle both up.
    :param matrix: payment matrix
    :return: simplified payment matrix
    """
    i_j_pairs = [[i, j] for i in range(4) for j in range(4) if i < j]
    for i_j_pair in i_j_pairs:
        i = i_j_pair[0]
        j = i_j_pair[1]
        if matrix[i][j] > matrix[j][i]:
            matrix[i][j] -= matrix[j][i]
            matrix[j][i] = 0
        else:
            matrix[j][i] -= matrix[i][j]
            matrix[i][j] = 0
    return matrix


def print_matrix(matrix):
    """
    Prints the 4x4 matrix
    :param matrix:
    :return:
    """
    for row in matrix:
        print("{e0}\t\t{e1}\t\t{e2}\t\t{e3}\n".format(e0=int(row[0]), e1=int(row[1]), e2=int(row[2]), e3=int(row[3])))
    print("--------------------------------------------------------------------------------")


def triangle_simplifier(simplified_matrix):
    """
    Implement Splitwise like polygon simplification on the matrix to reduce number of transactions needed to settle up.
    :param simplified_matrix:
    :return:
    """
    pass


def alex_maany_analyzer(group, expenses):
    alex = [x for x in group.members if x.first_name == "Alex"][0]
    maany = [x for x in group.members if x.first_name == "maany"][0]
    alex_maany_expenses = []
    for expense in expenses:
        user_id_array = [user.id for user in expense.users]
        if alex.id in user_id_array and maany.id in user_id_array:
            alex_maany_expenses.append(expense)

    # some metrics
    maany_net = sum([float(y.net_balance) for x in alex_maany_expenses for y in x.users if y.id == maany.id])
    alex_net = sum([float(y.net_balance) for x in alex_maany_expenses for y in x.users if y.id == alex.id])
    non_sfr = [x for x in alex_maany_expenses if x.description != 'SFR']
    maany_to_pay = 0
    maany_negative_transactions = []
    maany_positive_transactions = []
    wtf_transactions = []
    # detailed shit
    for expense in alex_maany_expenses:
        ###
        # paid by alex and amount owed by maany = x
        # paid my maany and amount owed by alex = y
        ###
        alex_expense_user = [user for user in expense.users if user.id == alex.id][0]
        maany_expense_user = [user for user in expense.users if user.id == maany.id][0]
        if float(alex_expense_user.net_balance) > 0 and float(maany_expense_user.net_balance) < 0:
            maany_to_pay = maany_to_pay + float(maany_expense_user.net_balance)
            maany_negative_transactions.append(expense)
        elif float(alex_expense_user.net_balance) < 0 and float(maany_expense_user.net_balance) > 0:
            maany_to_pay = maany_to_pay - float(alex_expense_user.net_balance)
            maany_positive_transactions.append(expense)
        else:
            wtf_transactions.append(expense)
            print("WTF WTF WTF WTF")

