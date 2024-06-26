# Generated from algoCode.g4 by ANTLR 4.13.1
import re
import time
from antlr4 import ParseTreeVisitor
from antlr4 import *
if "." in __name__:
    from .algoCodeParser import algoCodeParser
else:
    from algoCodeParser import algoCodeParser



# This class defines a complete generic visitor for a parse tree produced by algoCodeParser.

class algoCodeVisitor(ParseTreeVisitor):

    def __init__(self):
        self.context = [{}] 
        self.functions = []
        self.initA()
    def initA(self):
        self.context[-1]['A'] = {}
        self.context[-1]['A'][7] = 1
        self.context[-1]['A'][1] = 3
        self.context[-1]['A'][2] = 7
        self.context[-1]['A'][3] = 2
        self.context[-1]['A'][4] = 4
        self.context[-1]['A'][5] = 9
        self.context[-1]['A'][6] = 5

    def visitFunction_def(self, ctx:algoCodeParser.Function_defContext):
        function_name = ctx.TOK_VAR().getText()
        arguments = []
        statements = []
        return_statement = []

        arguments_ctx = ctx.arguments()
        if arguments_ctx:
            arguments = self.visitArguments(arguments_ctx)

        statement_ctxs = ctx.statement()
        for statement_ctx in statement_ctxs:
            statements.append(statement_ctx)

        return_statement = ctx.return_statement()
        self.functions.append(function_name)
        self.context[-1][function_name] = {}
        self.context[-1][function_name]["params"] = (arguments, statements, return_statement)

        

    
    
    def visitAssignment(self, ctx:algoCodeParser.AssignmentContext):
        if ctx.array_call():
            array_name = ctx.array_call().TOK_VAR().getText()
            index = self.visitExpression(ctx.array_call().expression())
            value = self.visitExpression(ctx.expression())
            #sprawdzam czy tablica zainicjowana
            if array_name not in self.context[-1].keys():
                self.context[-1][array_name] = {}
                print("tablica nie zdefiniowana")
                return None
            i = 1
            while len(self.context[-1][array_name]) < index:
                self.context[-1][array_name][i] = None
                i += 1
            self.context[-1][array_name][index] = value
        else:
            left_value = ctx.TOK_VAR()
            self.context[-1][left_value.getText()] = self.visitExpression(ctx.expression())

    
    def visitExpression(self, ctx: algoCodeParser.ExpressionContext):
            # If the expression is a variable
            if isinstance(ctx, TerminalNode):
                return ctx.getText()
            elif ctx.getChildCount() == 1:
                if ctx.TOK_VAR():
                    var_name = ctx.TOK_VAR().getText()
                    return self.context[-1].get(var_name, None)

                    
                    # If the expression is a number
                if ctx.TOK_NUM():
                    return int(ctx.TOK_NUM().getText())
                if ctx.array_call():
                    return self.visitArray_call(ctx.array_call())
                if ctx.function_call():
                    return self.visitFunction_call(ctx.function_call())
            
            # ten len token to chyba nie powinien istnieć wgl
            elif ctx.getChildCount() == 4:
                array_name = ctx.TOK_VAR().getText()
                if array_name in self.context[-1]:
                    return len(self.context[-1][array_name])
                else:
                    return None
        
        # jeśli działanie
            else:
                left_operand = self.visitExpression(ctx.expression(0))
                right_operand = self.visitExpression(ctx.expression(1))
                operator = ctx.getChild(1).getText()
                
                if left_operand != None and right_operand != None:
                    if operator == '+':
                        return left_operand + right_operand
                    elif operator == '-':
                        return left_operand - right_operand
                    elif operator == '/':
                        if right_operand != 0:
                            return left_operand / right_operand
                else:
                        # cholero nie dziel przez zero
                    return None


    # Visit a parse tree produced by algoCodeParser#bool_expression.
    def visitBool_expression(self, ctx:algoCodeParser.Bool_expressionContext):
        
        def visitVal(right_value):
            if isinstance(right_value, TerminalNode):
                right_value = right_value.getText()
                right_operand = self.context[-1].get(right_value, None)
                
                if right_value == '0':
                    right_operand = 0
                    return right_operand
                if right_operand == None:
                        right_operand = int(right_value)
                        return right_operand
                else:
                    return right_operand
            else:
                right_operand = self.visitArray_call(right_value)
                return right_operand

        def evaluate(operator, right_operand, left_operand):
            try:
                if operator == '==':
                    return left_operand == right_operand
                elif operator == '!=':
                    return left_operand != right_operand
                elif operator == '<':
                    return left_operand < right_operand
                elif operator == '>':
                    return left_operand > right_operand
                elif operator == '<=':
                    return left_operand <= right_operand
                elif operator == '>=':
                    return left_operand >= right_operand
            except:
                return False   
            
        i = 2
        outputs = []
        while i < ctx.getChildCount():
            left_value = ctx.getChild(i-2)
            right_value = ctx.getChild(i)
            right_operand = visitVal(right_value)
            left_operand = visitVal(left_value)
            operator = ctx.getChild(i-1).getText()
            outputs.append(evaluate(operator, right_operand, left_operand))
            i+=4

        # # If there are additional operations (e.g., AND or OR), continue evaluating
        operators = []
        output = outputs[0]
        if ctx.getChildCount() > 3:
            i = 3
            while i < ctx.getChildCount():
                 next_operator = ctx.getChild(i).getText()
                 operators.append(next_operator)     
                 i += 3
            for j in range(len(outputs)-1):
                if operators[j] == 'and':
                    output = output and outputs[j+1]
                elif operators[j] == 'or':
                    output = output or outputs[j+1]
        return output



    def visitFor_loop(self, ctx:algoCodeParser.For_loopContext):
        loop_var = ctx.TOK_VAR().getText()
        start = self.visitExpression(ctx.expression(0))
        end = self.visitExpression(ctx.expression(1))
        for current_value in range(start, end + 1):
            self.context[-1][loop_var] = current_value
            for statement in ctx.statement():
                self.visitStatement(statement)


    # Visit a parse tree produced by algoCodeParser#if_else_statement.
    def visitIf_else_statement(self, ctx:algoCodeParser.If_else_statementContext):
        condition = self.visitIf_statement(ctx.if_statement())
        else_statements = []
        if len(condition)==0 and ctx.else_statement():
            # Jeśli warunek if nie został spełniony i istnieje blok else
            else_statements = [self.visitStatement(child) for child in ctx.else_statement().statement()]
        return condition, else_statements



    # Visit a parse tree produced by algoCodeParser#else_statement.
    def visitElse_statement(self, ctx:algoCodeParser.Else_statementContext):
        return [self.visitStatement(child) for child in ctx.statement()]

    # Visit a parse tree produced by algoCodeParser#else_return_statement.
    def visitElse_return_statement(self, ctx:algoCodeParser.Else_return_statementContext):
        return self.visitReturn_statement(ctx.return_statement())


    # Visit a parse tree produced by algoCodeParser#if_return_statement.
    def visitIf_return_statement(self, ctx:algoCodeParser.If_return_statementContext):
        condition = self.visitIf_statement(ctx.if_statement())
        if condition:
            self.visitStatements(ctx.statement())
            return_value = self.visitReturn_statement(ctx.return_statement())
            return return_value



    # Visit a parse tree produced by algoCodeParser#if_statement.
    def visitIf_statement(self, ctx:algoCodeParser.If_statementContext):
        condition = self.visitBool_expression(ctx.bool_expression())
        statement_results = []
        if condition:
            for statement_ctx in ctx.statement():
                result = self.visitStatement(statement_ctx)
                statement_results.append(result)
        
        return statement_results


    def visitWhile_statement(self, ctx:algoCodeParser.While_statementContext):
        condition = self.visitBool_expression(ctx.bool_expression())
        start_time = time.time()
        max_duration = 5
        while condition:
            if time.time() - start_time > max_duration:
                print("RuntimeError")
                raise RuntimeError("Time limit exceeded for while loop execution")
            for statement in ctx.statement():
                self.visitStatement(statement)
            condition = self.visitBool_expression(ctx.bool_expression())
            

        
        
    def visitReturn_statement(self, ctx:algoCodeParser.Return_statementContext):
        value = self.context[-1].get(ctx.getChild(1).getText())
        return value
    
    def visitChildren(self, ctx):
        result = []
        for child in ctx.children:
            result.append(self.visit(child))
        return result
  
    
    def visitFunction_call(self, ctx:algoCodeParser.Function_callContext):
        func_name = ctx.TOK_VAR().getText()
        variables = ctx.arguments()
        arguments = self.visitArguments(ctx.arguments())
            # obsługa specjalnych funkcji, na razie tylko print
        if func_name.lower() == 'print':
            if type(arguments[0]) == dict:
                output = []
                for item in arguments[0]:
                    output.append(arguments[0][item])
                print(output)
            else:    
                #print(arguments)
                for arg in arguments:
                    print(arg)
        elif func_name == 'PARTITION':
            pass
        elif func_name == 'FLOOR':
            pass
        elif func_name == 'SWAP_VAR':
            if len(arguments) != 2:
                print("Error: SWAP function expects exactly two arguments.")
                return None
            args = ctx.arguments().getText()

            var1, var2 = args.split(',')
            # Retrieve the values from the context
            value1 = self.context[-1].get(var1)
            value2 = self.context[-1].get(var2)
            # Create copies of the values to avoid modifying the original references
            value1_copy = value1
            value2_copy = value2

            # Swap the values
            self.context[-1][var1] = value2_copy
            self.context[-1][var2] = value1_copy
        
        elif func_name == 'SWAP_ARRAY':
            if len(arguments) != 2:
                print("Error: SWAP function expects exactly two arguments.")
                return None
            values = self.visitArguments(ctx.arguments())
            val1, val2 = values[0], values[1]
            arr1 = ctx.arguments().argument()[0].expression().array_call().TOK_VAR().getText()
            idx1 = self.visitExpression(ctx.arguments().argument()[0].expression().array_call().expression())
            arr2 = ctx.arguments().argument()[1].expression().array_call().TOK_VAR().getText()
            idx2 = self.visitExpression(ctx.arguments().argument()[1].expression().array_call().expression())


            self.context[-1][arr1][idx1] = val2
            self.context[-1][arr2][idx2] = val1

        elif func_name == 'MIN_INDEX':
            if len(arguments) != 1:
                print("Error: MIN_INDEX function expects exactly 1 argument.")
                return None
            else:
                tab = ctx.arguments().argument()[0].expression().getText()
                min = 1
                for item in self.context[-1][tab]:
                    if self.context[-1][tab][item] < self.context[-1][tab][min]:
                        min = item
                return min

            # tutaj można dodać obsługę innych funkcji
        elif func_name in self.context[-1]:
            function_definition = self.context[-1][func_name]["params"]
            if arguments:
                if len(arguments) != len(function_definition[0]):
                    print(f"Error: Function '{func_name}' expects {len(function_definition[0])} arguments, but {len(arguments)} were provided.")
                    return None
            
            output = self.execute_statements(function_definition[0], arguments, function_definition[1], function_definition[2], func_name)
            if output:
                return output
        else:
            raise ValueError(f"Function '{func_name}' is not defined.")
        
    def execute_statements(self, func_args, call_args, func_statements, func_return, f_name):
        # dla kazdej funkcji słownik ze zmiennymi
        if call_args:
            for arg_name, arg_value in zip(func_args, call_args):
                self.context[-1][f_name][arg_name] = arg_value
        output = None
        for statement_ctx in func_statements:
            self.visitStatement(statement_ctx)
        if func_return:
            output = self.visitReturn_statement(func_return)
        return output
        
       
    # Visit a parse tree produced by algoCodeParser#program.
    def visitProgram(self, ctx):
        self.visitCode(ctx.code())


    # Visit a parse tree produced by algoCodeParser#code.
    def visitCode(self, ctx:algoCodeParser.CodeContext):
        if ctx.function_def():
            for child in ctx.function_def():
                self.visitFunction_def(child)        
        if ctx.statement():
            for child in ctx.statement():
                self.visitStatement(child)
                

    # Visit a parse tree produced by algoCodeParser#argument.
    def visitArgument(self, ctx:algoCodeParser.ArgumentContext):
        #zwracam dziecko czyli argument
        return self.visitExpression(ctx.expression())

    # Visit a parse tree produced by algoCodeParser#arguments.
    def visitArguments(self, ctx:algoCodeParser.ArgumentsContext):
        arguments = []
        # Przechodze przez każdy argument
        if ctx != None:
            if ctx.argument():
                for child in ctx.argument():
                    arguments.append(self.visitArgument(child))
            return arguments

    # Visit a parse tree produced by algoCodeParser#statement.
    def visitStatement(self, ctx: algoCodeParser.StatementContext):
        if ctx.assignment():
            return self.visitAssignment(ctx.assignment())
        elif ctx.array_def():
            return self.visitArray_def(ctx.array_def())
        elif ctx.function_call():
            return self.visitFunction_call(ctx.function_call())
        elif ctx.for_loop():
            return self.visitFor_loop(ctx.for_loop())
        elif ctx.if_statement():
            return self.visitIf_statement(ctx.if_statement())
        elif ctx.if_else_statement():
            return self.visitIf_else_statement(ctx.if_else_statement())
        elif ctx.if_return_statement():
            return self.visitIf_return_statement(ctx.if_return_statement())
        elif ctx.while_statement():
            return self.visitWhile_statement(ctx.while_statement())
        



    # Visit a parse tree produced by algoCodeParser#array_def.
    def visitArray_def(self, ctx:algoCodeParser.Array_defContext):
        #pobieram nazzwe tablicy i dodaje do kontekstu jako zainicjalizowana
        arr_name = ctx.TOK_VAR().getText()
        self.context[-1][arr_name] = {}
        print(f"Array defined: {arr_name} as empty dictionary")


    # Visit a parse tree produced by algoCodeParser#array_call.
    def visitArray_call(self, ctx:algoCodeParser.Array_callContext):
        arr_name = ctx.TOK_VAR().getText()
        #sprawdzam index w nawiasach
        index = self.visitExpression(ctx.expression())
        if index == 0:
            return 0

        if arr_name in self.context[-1]:
            if index in self.context[-1][arr_name]:
                return self.context[-1][arr_name].get(index)
            else:
                return [self.context[-1][arr_name][item] for item in self.context[-1][arr_name]]
        else:
            #jak nie to nic? tutaj chyba error by się przydał
            print("Invalid array")
   
        




del algoCodeParser
