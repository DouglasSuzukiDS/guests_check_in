class ClassOnlyMethod:
   #  Decorator que permite a chamada do método APENAS pela classe, bloqueando instâncias.
   def __init__(self, func):
      self.func = func

   def __get__(self, instance, owner=None):
      if instance is not None:
         raise AttributeError("Este método só pode ser chamado pela classe, não por uma instância.")
      return self.func.__get__(owner, owner)