from interpreter.parser import VariableStore as Store

# Util
def precedence(key):
  if key in ["+", "-"]:
    return 0
  elif key in ["*", "/", "%"]:
    return 1
  elif key in ["and", "or"]:
    return 2
  elif key in [">", ">=", "<", "<=", "==", "!="]:
    return 3
  elif key in ["not"]:
    return 4
  else:
    return 5

def toPostfix(data):
  stack = list()
  postfix = list()
  for i in data:
    if not i in ["+", "-", "*", "/", "%", "and", "or", "neg", "not", ">", ">=", "<", "<=", "==", "!=", "(", ")"]:
      postfix.append(i)
    else:
      if len(stack) == 0 or stack[-1] == "(":
        stack.append(i)
      elif i == "(":
        stack.append(i)
      elif i == ")":
        while stack[-1] != "(":
          postfix.append(stack.pop())
        stack.pop()
      elif precedence(stack[-1]) < precedence(i):
        stack.append(i)
      elif precedence(stack[-1]) == precedence(i):
        postfix.append(stack.pop())
        stack.append(i)
      elif precedence(stack[-1]) > precedence(i):
        postfix.append(stack.pop())
        data.insert(0, i)
  while len(stack) > 0:
    postfix.append(stack.pop())
  return postfix



def streamVExpr(expr):
  if expr[0] == "nop":
    return []
  return [expr[1]] + streamValue(expr[2])
def streamValue(expr):
  if expr[0] == "nop":
    return []
  if expr[1] == "-":
    return ["neg"] + streamValue(expr[2])
  elif expr[1] == "not":
    return ["not"] + streamValue(expr[2])
  key = expr[1][0]
  if key == "expr":
    return ["(", streamExpr(expr[1]), ")"]
  elif key == "int":
    return [expr[1][1]]
  elif key == "id":
    return [expr[1][1]]
def streamFExpr(expr):
  if expr[0] == "nop":
    return []
  return [expr[1]] + streamTerm(expr[2])
def streamFactor(expr):
  if expr[0] == "nop":
    return []
  return streamValue(expr[1]) + streamVExpr(expr[2])
def streamTerm(expr):
  if expr[0] == "nop":
    return []
  return streamFactor(expr[1]) + streamFExpr(expr[2])
def streamTExpr(expr):
  if expr[0] == "nop":
    return []
  return [expr[1]] + streamNExpr(expr[2])
def streamBExpr(expr):
  if expr[0] == "nop":
    return []
  return [expr[1]] + streamNExpr(expr[2])
def streamNExpr(expr):
  if expr[0] == "nop":
    return []
  return streamTerm(expr[1]) + streamTExpr(expr[2])
def streamExpr(expr):
  if expr[0] == "nop":
    return []
  return streamNExpr(expr[1]) + streamBExpr(expr[2])
def stretchExpr(stream):
  newStream = list()
  for i in stream:
    if type(i) == list:
      newStream += stretchExpr(i)
    else:
      newStream.append(i)
  return newStream

def resolveExpr(expr, store: Store):
  stream = streamExpr(expr)
  stream = stretchExpr(stream)
  postfix = toPostfix(stream)
  #print(stream)
  #print(postfix)
  stack = list()
  for i in postfix:
    if i.isdigit() or i[1:].isdigit():
      stack.append(int(i))
    elif store.getVar(i) != None:
      stack.append(int(store.getVar(i)))
    else:
      if i == "+":
        if len(stack) < 2:
          break
        stack.append(stack.pop() + stack.pop())
      elif i == "-":
        if len(stack) < 2:
          break
        j = stack.pop()
        stack.append(stack.pop() - j)
      elif i == "*":
        if len(stack) < 2:
          break
        stack.append(stack.pop() * stack.pop())
      elif i == "/":
        if len(stack) < 2:
          break
        j = stack.pop()
        stack.append(stack.pop() / j)
      elif i == "%":
        if len(stack) < 2:
          break
        j = stack.pop()
        stack.append(stack.pop() % j)
      elif i == "and":
        if len(stack) < 2:
          break
        stack.append(int(stack.pop() and stack.pop()))
      elif i == "or":
        if len(stack) < 2:
          break
        stack.append(int(stack.pop() or stack.pop()))
      elif i == "neg":
        if len(stack) < 1:
          break
        stack.append(-stack.pop())
      elif i == "not":
        if len(stack) < 1:
          break
        stack.append(int(not stack.pop()))
      elif i == ">":
        if len(stack) < 2:
          break
        j = stack.pop()
        stack.append(int(stack.pop() > j))
      elif i == ">=":
        if len(stack) < 2:
          break
        j = stack.pop()
        stack.append(int(stack.pop() >= j))
      elif i == "<":
        if len(stack) < 2:
          break
        j = stack.pop()
        stack.append(int(stack.pop() < j))
      elif i == "<=":
        if len(stack) < 2:
          break
        j = stack.pop()
        stack.append(int(stack.pop() <= j))
      elif i == "==":
        if len(stack) < 2:
          break
        stack.append(int(stack.pop() == stack.pop()))
      elif i == "!=":
        if len(stack) < 2:
          break
        stack.append(int(stack.pop() != stack.pop()))
  return stack.pop()



def interpretWhile(command, store: Store):
  condition = resolveExpr(command[1], store)
  while condition != 0:
    interpret(command[2], store)
    condition = resolveExpr(command[1], store)

def interpretShift(command, store: Store):
  store.setVar(command[1], int(store.getVar(command[1])) >> resolveExpr(command[2], store))

def interpretGet(command, store: Store):
  store.setVar(command[1], input("{0}...".format(command[1])))

def interpretIf(command, store: Store):
  condition = resolveExpr(command[1], store)
  if condition != 0:
    interpret(command[2], store)
  else:
    interpret(command[3], store)

def interpretExit(command, store: Store):
  exit(resolveExpr(command[1], store))

def interpretSet(command, store: Store):
  store.setVar(command[1], resolveExpr(command[2], store))

def interpretPrint(command, newLine: bool, store: Store):
  arg = command[1]
  if arg[0] == "string":
    print(arg[1], end="" if not newLine else "\n")
  elif arg[0] == "expr":
    print(resolveExpr(arg, store), end="" if not newLine else "\n")

def interpret(program, store: Store):
  store.push()
  for command in program:
    cmdType = command[0]
    if cmdType == "nop":
      continue
    elif cmdType == "get":
      interpretGet(command, store)
    elif cmdType == "exit":
      interpretExit(command, store)
    elif cmdType == "print":
      interpretPrint(command, False, store)
    elif cmdType == "println":
      interpretPrint(command, True, store)
    elif cmdType == "shift":
      interpretShift(command, store)
    elif cmdType == "set":
      interpretSet(command, store)
    elif cmdType == "if":
      interpretIf(command, store)
    elif cmdType == "while":
      interpretWhile(command, store)
  store.pop()