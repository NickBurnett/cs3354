from interpreter.lexer import OutputType, LexOutput

# UTILITY

class VariableStore:
  def __init__(self):
    self.store = list()
    self.push()
  
  def push(self):
    self.store.append(dict())
  
  def pop(self):
    self.store.pop()
  
  def setVar(self, var, val = 0):
    for i in range(len(self.store) - 1, -1, -1):
      d = self.store[i]
      if var in d:
        d[var] = val
    self.store[-1][var] = val
  
  def getVar(self, var):
    for i in range(len(self.store) - 1, -1, -1):
      d = self.store[i]
      if var in d:
        return d[var]
    return None

class ParseOutput:
  def __init__(self, success: bool, data):
    self.success = success
    self.data = data


tokens = []
store: VariableStore
debugging: bool = False

def debug(t: str, token: LexOutput):
  if not debugging:
    return
  if not token:
    print("{0}".format(t))
    return
  print("{0}: {1} {2}".format(t, token.output_type, token.output))

def error(token: LexOutput):
  print("Unexpected token '{0}' on line {1}".format(token.output, token.token_line))

def next() -> LexOutput:
  global tokens
  if len(tokens) <= 0:
    return LexOutput(OutputType.NONE, "End-of-line", -1, "")
  token = tokens[0]
  tokens = tokens[1:]
  return token

def revert(token):
  tokens.insert(0, token)

# PARSING
def parseValue():
  token = next()
  debug("value", token)
  if token.output_type != OutputType.LEXEME and token.output_type != OutputType.TOKEN_KEYWORD and token.output_type != OutputType.TOKEN_ID and token.output_type != OutputType.TOKEN_INT:
    error(token)
    return False
  if token.output_type == OutputType.TOKEN_ID:
    if store.getVar(token.output) == None:
      error(token)
      return False
    return ["value", ["id", token.output]]
  elif token.output_type == OutputType.TOKEN_INT:
    return ["value", ["int", token.output]]
  elif token.output == "-":
    value = parseValue()
    if value == False:
      return False
    return ["value", "-", value]
  elif token.output == "not":
    value = parseValue()
    if value == False:
      return False
    return ["value", "not", value]
  elif token.output == "(":
    expr = parseExpr()
    if expr == False or next().output != ")":
      return False
    return ["value", expr]
  else:
    error(token)
    return False

def parseVExpr():
  token = next()
  debug("v_expr", token)
  if token.output_type != OutputType.LEXEME:
    revert(token)
    debug("revert", None)
    return ["nop"]
  if token.output == ">":
    value = parseValue()
    if value == False:
      return False
    return ["v_expr", ">", value]
  elif token.output == ">=":
    value = parseValue()
    if value == False:
      return False
    return ["v_expr", ">=", value]
  elif token.output == "<":
    value = parseValue()
    if value == False:
      return False
    return ["v_expr", "<", value]
  elif token.output == "<=":
    value = parseValue()
    if value == False:
      return False
    return ["v_expr", "<=", value]
  elif token.output == "==":
    value = parseValue()
    if value == False:
      return False
    return ["v_expr", "==", value]
  elif token.output == "!=":
    value = parseValue()
    if value == False:
      return False
    return ["v_expr", "!=", value]
  else:
    revert(token)
    debug("revert", None)
    return ["nop"]

def parseFExpr():
  token = next()
  debug("f_expr", token)
  if token.output_type != OutputType.LEXEME:
    revert(token)
    debug("revert", None)
    return ["nop"]
  if token.output == "*":
    term = parseTerm()
    if term == False:
      return False
    return ["f_expr", "*", term]
  elif token.output == "/":
    term = parseTerm()
    if term == False:
      return False
    return ["f_expr", "/", term]
  elif token.output == "%":
    term = parseTerm()
    if term == False:
      return False
    return ["f_expr", "%", term]
  else:
    revert(token)
    debug("revert", None)
    return ["nop"]

def parseFactor():
  debug("factor", None)
  value = parseValue()
  if value == False:
    return False
  vExpr = parseVExpr()
  if vExpr == False:
    return False
  return ["factor", value, vExpr]

def parseTExpr():
  token = next()
  debug("t_expr", token)
  if token.output_type != OutputType.LEXEME:
    revert(token)
    debug("revert", None)
    return ["nop"]
  if token.output == "+":
    nExpr = parseNExpr()
    if nExpr == False:
      return False
    return ["t_expr", "+", nExpr]
  elif token.output == "-":
    nExpr = parseNExpr()
    if nExpr == False:
      return False
    return ["t_expr", "-", nExpr]
  else:
    revert(token)
    debug("revert", None)
    return ["nop"]

def parseTerm():
  debug("term", None)
  factor = parseFactor()
  if factor == False:
    return False
  fExpr = parseFExpr()
  if fExpr == False:
    return False
  return ["term", factor, fExpr]

def parseBExpr():
  token = next()
  debug("b_expr", token)
  if token.output_type != OutputType.TOKEN_KEYWORD:
    revert(token)
    debug("revert", None)
    return ["nop"]
  if token.output == "and":
    nExpr = parseNExpr()
    if nExpr == False:
      return False
    return ["b_expr", "and", nExpr]
  elif token.output == "or":
    nExpr = parseNExpr()
    if nExpr == False:
      return False
    return ["b_expr", "or", nExpr]
  else:
    revert(token)
    debug("revert", None)
    return ["nop"]

def parseNExpr():
  debug("n_expr", None)
  term = parseTerm()
  if term == False:
    return False
  tExpr = parseTExpr()
  if tExpr == False:
    return False
  return ["n_expr", term, tExpr]

def parseExpr():
  debug("expression", None)
  nExpr = parseNExpr()
  if nExpr == False:
    return False
  bExpr = parseBExpr()
  if bExpr == False:
    return False
  return ["expr", nExpr, bExpr]

def parseExitArg():
  expr = parseExpr()
  if expr == False:
    return False
  return expr

def parseShiftArg():
  token = next()
  if token.output_type != OutputType.TOKEN_ID or store.getVar(token.output) == None:
    error(token)
    return False
  if next().output != ",":
    return False
  expr = parseExpr()
  if expr == False:
    return False
  return [token.output, expr]

def parsePrintArg():
  token = next()
  debug("print", token)
  if token.output_type == OutputType.TOKEN_STRING:
    return ["string", token.output]
  revert(token)
  expr = parseExpr()
  if expr == False:
    return False
  return expr

def parseStmt():
  token = next()
  debug("stmt", token)
  if token.output_type != OutputType.TOKEN_KEYWORD and token.output_type != OutputType.TOKEN_ID:
    error(token)
    return False
  if token.output == "else":
    revert(token)
    debug("revert", None)
    return ["nop"]
  elif token.output == "end":
    revert(token)
    debug("revert", None)
    return ["nop"]
  elif token.output == "print":
    printCmd = parsePrintArg()
    if printCmd == False:
      return False
    return ["print", printCmd]
  elif token.output == "println":
    printCmd = parsePrintArg()
    if printCmd == False:
      return False
    return ["println", printCmd]
  elif token.output == "shift":
    shiftCmd = parseShiftArg()
    if shiftCmd == False:
      return False
    return ["shift"] + shiftCmd
  elif token.output == "exit":
    exitCmd = parseExitArg()
    if exitCmd == False:
      return False
    return ["exit", exitCmd]
  elif token.output == "get":
    token = next()
    if token.output_type != OutputType.TOKEN_ID:
      return False
    store.setVar(token.output)
    return ["get", token.output]
  elif token.output_type == OutputType.TOKEN_ID:
    oldToken = token
    token = next()
    if token.output != "=":
      return False
    expr = parseExpr()
    if expr == False:
      return False
    store.setVar(oldToken.output)
    return ["set", oldToken.output, expr]
  elif token.output == "if":
    store.push()
    expr = parseExpr()
    if expr == False or next().output != "then":
      return False
    thenList = parseStmtList()
    if thenList == False or next().output != "else":
      return False
    store.push()
    elseList = parseStmtList()
    if elseList == False or next().output != "end":
      return False
    return ["if", expr, thenList, elseList]
  elif token.output == "while":
    store.push()
    expr = parseExpr()
    if expr == False or next().output != "do":
      return False
    stmtList = parseStmtList()
    if stmtList == False or next().output != "end":
      return False
    return ["while", expr, stmtList]
  else:
    error(token)
    return False

def parseStmtList():
  token = next()
  debug("stmt_list", token)
  if token.output_type == OutputType.NONE:
    return [["nop"]]
  revert(token)
  stmt = parseStmt()
  if stmt == False:
    return False
  token = next()
  if token.output != ";":
    error(token)
    return False
  token = next()
  if token.output == "else" or token.output == "end":
    revert(token)
    store.pop()
    return [stmt]
  else:
    revert(token)
  stmtList = parseStmtList()
  if stmtList == False:
    return False
  return [stmt] + stmtList

def parseProgram(lexed_tokens, varStore, debug = False):
  global tokens
  global store
  global debugging
  store = varStore
  debugging = debug
  if len(lexed_tokens) <= 0:
    return False
  tokens = lexed_tokens
  store.push()
  stmtList = parseStmtList()
  if stmtList == False:
    return False
  store.pop()
  return stmtList
