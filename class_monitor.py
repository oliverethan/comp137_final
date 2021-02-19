#NAP Class Monitor
class Class_Monitor():
  def __init__(self, num_neurons, class_weights, bdd, split, varname):
    # init empty pattern set
    self.patterns = bdd.false

    self.num_neurons = num_neurons
    self.varname = varname

    # find the most influencial weights for that class
    top_indices = np.argsort(class_weights)

    # decide if selecting all positive neurons or a split of negative and positive
    if split == 0:
      self.indices = top_indices[(-num_neurons):]
    else:
      top_split = top_indices[:split]
      bottom_split = top_indices[(-(num_neurons-split)):]
      self.indices = np.concatenate((top_split, bottom_split))
      print(self.indices.shape)

  def addpattern(self, bdd,  neuron_pattern):
      selected_pattern = neuron_pattern[self.indices]

      # Generate constraint
      pattern_gen = ""
      for i in range(self.num_neurons):
        if i != 0:
          pattern_gen = pattern_gen + " & "

        if selected_pattern[i]:
          pattern_gen = pattern_gen + self.varname + str(i)
        else:
          pattern_gen = pattern_gen + "!" + self.varname + str(i)

      # Encode into bdd
      self.patterns = self.patterns | bdd.add_expr(pattern_gen)

  def ispattern(self, bdd,  neuron_pattern):
      selected_pattern = neuron_pattern[self.indices]

      # Generate constraint
      pattern_gen = ""
      for i in range(self.num_neurons):
        if i != 0:
          pattern_gen = pattern_gen + " & "

        if selected_pattern[i]:
          pattern_gen = pattern_gen + self.varname + str(i)
        else:
          pattern_gen = pattern_gen + "!" + self.varname + str(i)

      #Check if pattern is in patterns    
      if ( self.patterns & bdd.add_expr(pattern_gen)) == bdd.false :            
          return False
      else:
          return True

  def enlargeset(self, bdd):
    enlargedpatterns = self.patterns
    for i in range(self.num_neurons):
        #add a pattern with one var changed for each var
        enlargedpatterns = enlargedpatterns | bdd.exist([self.varname + str(i)], self.patterns)
    self.patterns = enlargedpatterns  