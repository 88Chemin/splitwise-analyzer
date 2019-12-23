from flask import Flask, render_template, redirect, session, url_for, request
from splitwise import Splitwise
import config as Config
import datetime
from copy import copy, deepcopy


app = Flask(__name__)
app.secret_key = "test_secret_key"

@app.route("/")
def home():
    if 'access_token' in session:
        return redirect(url_for("analyzer"))
    return render_template("home.html")

@app.route("/login")
def login():

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    return redirect(url)


@app.route("/authorize")
def authorize():

    if 'secret' not in session:
        return redirect(url_for("home"))

    oauth_token    = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    access_token = sObj.getAccessToken(oauth_token,session['secret'],oauth_verifier)
    session['access_token'] = access_token

    return redirect(url_for("analyzer"))


@app.route("/friends")
def friends():
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    friends = sObj.getFriends()
    return render_template("friends.html",friends=friends)


@app.route("/analyze")
def analyzer():
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    groups = sObj.getGroups()
    group = [ x for x in groups if x.name == "88 Chemin 2018"][0]

    expenses = sObj.getExpenses(group_id=group.id, limit=10000, dated_after=datetime.datetime(2017,5, 1))
    matrix = payment_matrix(group, expenses)

    return "Check console"


def payment_matrix(group, expenses):
    """
              alex danny maany patrick
            ___________________________
    alex    |
    danny   |
    maany   |
    patrick |

    :param group: splitwise group object
    :param expenses: group expenses
    :return:
    """
    matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    # alex, danny, maany, patrick = [None] * 4
    #
    # for user in group.members:
    #     alex = user if user.first_name == "Alex" else alex
    #     danny = user if user.first_name == "Daniel" else danny
    #     maany = user if user.first_name == "maany" else maany
    #     patrick = user if user.first_name == "Patrick" else patrick
    #
    # users = [alex, danny, maany, patrick]

    # def get_user(first_name):
    #     if first_name == "Alex":
    #         return alex
    #     elif first_name == "Daniel":
    #         return daany
    #     elif first_name == "maany":
    #         return maany
    #     else:
    #         return patrick

    def get_index_for_dude(dude):
        if dude.first_name == "Alex":
            return 0
        elif dude.first_name == "Daniel":
            return 1
        elif dude.first_name == "Patrick":
            return 2
        elif dude.first_name == "maany":
            return 3

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
    print_matrix(matrix)
    simplified_matrix = simplify_matrix(matrix)
    print_matrix(simplified_matrix)
    return matrix


def simplify_matrix(matrix):
    simple_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
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
    print_matrix(matrix)
    return simple_matrix


def print_matrix(matrix):
    for row in matrix:
        print("{e0}\t\t{e1}\t\t{e2}\t\t{e3}\n".format(e0=int(row[0]), e1=int(row[1]), e2=int(row[2]), e3=int(row[3])))
    print("--------------------------------------------------------------------------------")


def splitwise_simplifier(simplified_matrix):
    spl_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for current_user in range(4):
        for user_owed_to in [x for x in range(4) if x != current_user]:
            if current_user

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


if __name__ == "__main__":
    app.run(threaded=True,debug=True)
