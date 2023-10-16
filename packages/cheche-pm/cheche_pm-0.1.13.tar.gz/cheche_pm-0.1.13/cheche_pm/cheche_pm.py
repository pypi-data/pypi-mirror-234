"""Main module. Contains the object Project."""
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx
import warnings
import pydot
import matplotlib.image as mpimg
import matplotlib.dates as mdates
import datetime
import plotly.express as px
import copy
from scipy import stats
import random
from itertools import chain, combinations

class Project():

  def __init__(self, n_activities=None, n_resources=None,activities = None,a_desc = None,a_duration = None,a_cost = None,a_precedence = None,a_resources = None,max_resources = None,G = None,dummies = False):

    self.n_activities = n_activities if n_activities is not None else 0
    self.n_resources = n_resources if n_resources is not None else 0
    self.N = self.n_activities + 2
    self.end_idx = self.N - 1
    self.activities = activities if activities is not None else []
    self.a_desc = a_desc if a_desc is not None else []
    self.a_duration = a_duration if a_duration is not None else []
    self.a_cost = a_cost if a_cost is not None else []
    self.a_precedence = a_precedence if a_precedence is not None else []
    self.a_resources = a_resources if a_resources is not None else []
    if n_activities:
      self.a_idx = list(range(1,len(activities) +1))
    else:
      self.activity_counter = len(self.activities) +1
    self.max_resources = max_resources if max_resources is not None else []
    self.graph = G if G is not None else {}
    self.PROJECT = {}
    self.cpm_schedule = {}
    self.dummies_added = dummies

  def add_activity(self,activity_name,activity_duration,activity_precedence,a_desc = 'Activity',activity_cost = 0,activity_resources = -1):

    """
        Add an activity to the project.

        Parameters
        ----------
        activity_name : str
            The name of the activity to be added.

        activity_duration : int or float
            The duration of the activity in time units (e.g., days).

        activity_precedence : list of str
            A list of activity names that this activity depends on.

        a_desc : str, optional
            A description for the activity (default is 'Activity').

        activity_cost : int or float, optional
            The cost associated with the activity (default is 0).

        activity_resources : int or float or list of int or float, optional
            The resource requirements for the activity. If a single value is provided,
            it is assumed to be the resource requirement for all resources. If a list
            is provided, it should specify the resource requirements for each resource.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the activity name is already in the project activities.

            If the number of resources does not match the number of resources recorded
            for previously created activities.

        Notes
        -----
        - If `a_desc` is set to 'Activity', it will be automatically replaced with
          'Activity_{activity_name}'.

        - If `activity_resources` is provided and this is the first activity added
          to the project, the number of resources for the project will be set to
          match the provided resource requirements.

        - Subsequent activities must have resource requirements matching the number
          of resources set for the project.

        - The activity is added to the project with a unique index.

        Examples
        --------
        >>> project = Project()
        >>> project.add_activity('Task1', 5, ['Predecessor1', 'Predecessor2'], 'Custom Task', 100, [10, 20, 30])
        >>> project.add_activity('Task2', 3, ['Task1'], 'Another Task', 50)
        """

    if activity_name in self.activities:
      raise ValueError(f'Activity {activity_name} already in project activities {self.activities}')

    self.activities.append(activity_name)
    self.a_duration.append(activity_duration)
    self.a_precedence.append(activity_precedence)
    self.a_cost.append(activity_cost)

    if a_desc == 'Activity':
      a_desc = f'{a_desc}_{activity_name}'
      self.a_desc.append(a_desc)
    else:
      self.a_desc.append(a_desc)
    if activity_resources != -1:
      if self.n_resources == 0:
        if isinstance(activity_resources, list):
          self.a_resources.append(activity_resources)
        if not isinstance(activity_resources, list):
          self.a_resources.append([activity_resources])
        self.n_resources = len(activity_resources)
        self.max_resources = [0]*self.n_resources
      else:
        if len(activity_resources) != self.n_resources:
          raise ValueError(f'The number of resources does not match the number of resources recorded for previously created activities ({self.n_resources})')
        else:
          self.a_resources.append(activity_resources)

    self.activity_counter += 1
    self.n_activities = len(self.activities)
    self.a_idx = list(range(1,self.n_activities +1))

  def delete_activity(self,activity_name):

    """
        Delete an activity from the project.

        Parameters
        ----------
        activity_name : str
            The name of the activity to be deleted.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the activity name is not found in the project activities.

        Notes
        -----
        - This method removes an activity from the project based on its name.

        - The activity counter is decremented, and the activity index list is updated
          after deletion.

        Examples
        --------
        >>> project = Project()
        >>> project.add_activity('Task1', 5, ['Predecessor1', 'Predecessor2'], 'Custom Task', 100, [10, 20, 30])
        >>> project.add_activity('Task2', 3, ['Task1'], 'Another Task', 50)
        >>> project.delete_activity('Task1')
        >>> len(project.activities)
        1
        >>> len(project.a_duration)
        1
        >>> len(project.a_precedence)
        1
        >>> len(project.a_cost)
        1
        >>> len(project.a_desc)
        1
        >>> len(project.a_resources)
        0
        >>> project.activity_counter
        1
        >>> project.n_activities
        1
        >>> project.a_idx
        [1]
        """

    if activity_name not in self.activities:
      raise ValueError(f'Activity {activity_name} not found in project activities {self.activities}')
    else:
      idx = self.activities.index(activity_name)
      self.activities.pop(idx)
      self.a_duration.pop(idx)
      self.a_precedence.pop(idx)
      self.a_cost.pop(idx)
      self.a_desc.pop(idx)
      if self.n_resources != 0:
        self.a_resources.pop(idx)
      self.activity_counter -= 1
      self.n_activities = len(self.activities)
      self.a_idx = list(range(1,self.n_activities +1))



  def add_dummies_create_project_network(self):

    """
        Add dummy 'Start' and 'End' nodes to create the project network.

        This method adds 'Start' and 'End' nodes to the project network if they
        are not already present. The 'Start' node has a duration of 0, no
        resources, and zero cost. The 'End' node has no outgoing edges, making
        it a terminal node.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If 'Start' and 'End' nodes (dummies) are already added to the project.

        Notes
        -----
        - This method extends the project network by adding 'Start' and 'End' nodes
          and connecting them to the existing activities based on their precedence.

        - Resource requirements for the dummy nodes are set to zero.

        Examples
        --------
        >>> project = Project()
        >>> project.add_activity('Task1', 5, ['Predecessor1', 'Predecessor2'], 'Custom Task', 100, [10, 20, 30])
        >>> project.add_dummies_create_project_network()
        >>> 'Start' in project.activities
        True
        >>> 'End' in project.activities
        True
        """

    if self.dummies_added:
      raise ValueError("Dummy \"Start\" and \"End\" already in Project")

    def one_hot_resources(lista):
      output = []
      for x in lista:
        output += x
      options = sorted(list(set(output)))
      #print(options)

      one_hot = [[0]*len(options) for x in range(len(lista))]
      for i,row in enumerate(lista):
        for x in row:
          idx = options.index(x)
          one_hot[i][idx] = 1

      return one_hot

    activities = self.activities
    activities = ['Start'] + activities + ['End']
    durations = self.a_duration
    durations = [0] + durations + [0]
    resources = self.a_resources
    precedence = self.a_precedence
    precedence = [x[0] for x in precedence]
    precedence = ['Start' if pd.isna(x) else x for x in precedence]
    precedence = [x.split(",") for x in precedence]
    precedence = [None] + precedence + [None]
    if isinstance(resources[0][0],str):
      resources = one_hot_resources(resources)
      n_r = len(resources[0])
      resources = [[0]*n_r] + resources + [[0]*n_r]
    else:
      n_r = self.n_resources
      resources = [[0]*n_r] + resources + [[0]*n_r]
    cost = [0] + self.a_cost + [0]

    description = self.a_desc
    description = ['Start of Project'] + description +  ['End of Project']

    EDGES = []
    for a,prec in zip(activities,precedence):
      if prec == None:
        continue

      for pr in prec:
        if pr == None:
          continue
        EDGES.append((pr,a))

    G = nx.DiGraph()
    G.add_nodes_from(activities)
    G.add_edges_from(EDGES)

    end_prec = []
    for node in activities:
      if node == 'End':
        continue
      if len(nx.descendants(G, node)) == 0:
        G.add_edge(node, 'End')
        end_prec.append(node)
    precedence[-1] = end_prec

    self.activities = activities
    self.a_precedence = precedence
    self.a_duration = durations
    self.a_resources = resources
    self.n_resources = n_r
    self.a_cost = cost
    self.a_desc = description
    self.n_activities = len(self.activities)
    self.a_idx = list(range(1,self.n_activities +1))
    self.graph = G
    self.dummies_added = True


  @classmethod
  def from_csv(cls,filename,rcpsp_format = True ,n_resources = 0,max_resources = []):

    """
        Create a Project instance from data in a CSV file.

        This class method creates a new instance of the Project class using data
        loaded from a CSV file. The CSV file must have specific columns with the
        following names: ['activity', 'description', 'duration', 'precedence', 'cost'].
        If `rcpsp_format` is True, the last columns must represent a dummy encoding
        of resource consumption for each activity.

        Parameters
        ----------
        filename : str
            The name of the CSV file to read, including the .csv file extension.

        rcpsp_format : bool, optional
            If True, the resource information is given as a dummy encoding of resources.
            If False, the resource column contains the names of the resources assigned
            for each activity. Default is True.

        n_resources : int, optional
            The number of resources that the project uses. This only applies if
            `rcpsp_format` is True, as it determines the number of columns to read
            for resources. If `rcpsp_format` is False, this parameter is ignored.
            Default is 0.

        max_resources : list of int, optional
            The resource maximum limit for each resource consumed by the project.
            Default is an empty list.

        Returns
        -------
        Project
            A new instance of the Project class with the terminal nodes added and
            its initialization arguments filled.

        Raises
        ------
        ValueError
            If 'Start' and 'End' nodes (dummies) are already added to the project.

        Notes
        -----
        - This method reads data from a CSV file and constructs a project network
          based on the provided data, adding 'Start' and 'End' nodes.

        - Resource requirements and maximum limits are set based on the CSV data.

        Examples
        --------
        >>> project = Project.from_csv('project_data.csv')
        >>> project.activities
        ['Start', 'Activity1', 'Activity2', 'End']
        >>> project.a_duration
        [0, 5, 3, 0]
        >>> project.a_cost
        [0, 100, 0, 0]
        >>> len(project.a_resources)
        4
        >>> project.n_resources
        2
        >>> 'Start' in project.graph.nodes
        True
        >>> 'End' in project.graph.nodes
        True
        """

    def one_hot_resources(lista):
      output = []
      for x in lista:
        output += x
      options = sorted(list(set(output)))
      #print(options)

      one_hot = [[0]*len(options) for x in range(len(lista))]
      for i,row in enumerate(lista):
        for x in row:
          idx = options.index(x)
          one_hot[i][idx] = 1

      return one_hot

    df = pd.read_csv(filename)
    n = len(df)
    n_r = n_resources
    activities = df['activity'].tolist()
    activities = ['Start'] + activities + ['End']
    precedence = df['precedence'].tolist()
    precedence = ['Start' if pd.isna(x) else x for x in precedence]
    precedence = [x.split(",") for x in precedence]
    precedence = [None] + precedence + [None]
    durations = [0] + df['duration'].tolist() + [0]
    if rcpsp_format:
      if n_r > 0:
        resources = df.iloc[:,-n_r:].values.tolist()
        resources = [[0]*n_r] + resources + [[0]*n_r]
      else:
        resources = []
      if not max_resources:
        max_resources = n_r*[np.inf]
      else:
        max_resources = max_resources
    if not rcpsp_format:

      resources = df['resources'].tolist()
      resources = [x.strip().split(",") for x in resources]
      resources = one_hot_resources(resources)
      n_r = len(resources[0])
      resources = [[0]*n_r] + resources + [[0]*n_r]

      if not max_resources:
        max_resources = [1]*n_r
      else:
        max_resources = max_resources

    if 'cost' in df.columns:
      cost = [0] + df['cost'].tolist() + [0]
    else:
      cost = [0] + [0]*n + [0]

    if 'description' in df.columns:
      description = ['Start of Project'] + df['description'].tolist() + ['End of Project']
    else:
      description = ['Start of Project'] + [f'Activity_{x}' for x in activities] + ['End of Project']

    EDGES = []
    for a,prec in zip(activities,precedence):
      if prec == None:
        continue

      for pr in prec:
        if pr == None:
          continue
        EDGES.append((pr,a))

    G = nx.DiGraph()
    G.add_nodes_from(activities)
    G.add_edges_from(EDGES)

    end_prec = []
    for node in activities:
      if node == 'End':
        continue
      if len(nx.descendants(G, node)) == 0:
        G.add_edge(node, 'End')
        end_prec.append(node)
    precedence[-1] = end_prec

    return cls(n_activities = n,n_resources = n_r,activities=activities,
               a_desc = description,a_duration = durations,a_cost = cost,a_precedence = precedence,
               a_resources = resources,max_resources = max_resources,G = G,dummies = True)

  @classmethod
  def from_excel(cls,filename,rcpsp_format = True ,n_resources = 0,max_resources = []):

    """
        Create a Project instance from data in a EXCEL (.xlsx) file.

        This class method creates a new instance of the Project class using data
        loaded from a EXCEL file. The EXCEL file must have specific columns with the
        following names: ['activity', 'description', 'duration', 'precedence', 'cost'].
        If `rcpsp_format` is True, the last columns must represent a dummy encoding
        of resource consumption for each activity.

        Parameters
        ----------
        filename : str
            The name of the EXCEL file to read, including the .xlsx file extension.

        rcpsp_format : bool, optional
            If True, the resource information is given as a dummy encoding of resources.
            If False, the resource column contains the names of the resources assigned
            for each activity. Default is True.

        n_resources : int, optional
            The number of resources that the project uses. This only applies if
            `rcpsp_format` is True, as it determines the number of columns to read
            for resources. If `rcpsp_format` is False, this parameter is ignored.
            Default is 0.

        max_resources : list of int, optional
            The resource maximum limit for each resource consumed by the project.
            Default is an empty list.

        Returns
        -------
        Project
            A new instance of the Project class with the terminal nodes added and
            its initialization arguments filled.

        Raises
        ------
        ValueError
            If 'Start' and 'End' nodes (dummies) are already added to the project.

        Notes
        -----
        - This method reads data from a CSV file and constructs a project network
          based on the provided data, adding 'Start' and 'End' nodes.

        - Resource requirements and maximum limits are set based on the CSV data.

        Examples
        --------
        >>> project = Project.from_csv('project_data.xlsx')
        >>> project.activities
        ['Start', 'Activity1', 'Activity2', 'End']
        >>> project.a_duration
        [0, 5, 3, 0]
        >>> project.a_cost
        [0, 100, 0, 0]
        >>> len(project.a_resources)
        4
        >>> project.n_resources
        2
        >>> 'Start' in project.graph.nodes
        True
        >>> 'End' in project.graph.nodes
        True
        """

    def one_hot_resources(lista):
      output = []
      for x in lista:
        output += x
      options = sorted(list(set(output)))
      #print(options)

      one_hot = [[0]*len(options) for x in range(len(lista))]
      for i,row in enumerate(lista):
        for x in row:
          idx = options.index(x)
          one_hot[i][idx] = 1

      return one_hot

    df = pd.read_excel(filename)
    n = len(df)
    n_r = n_resources
    activities = df['activity'].tolist()
    activities = ['Start'] + activities + ['End']
    precedence = df['precedence'].tolist()
    precedence = ['Start' if pd.isna(x) else x for x in precedence]
    precedence = [x.split(",") for x in precedence]
    precedence = [None] + precedence + [None]
    durations = [0] + df['duration'].tolist() + [0]
    if rcpsp_format:
      if n_r > 0:
        resources = df.iloc[:,-n_r:].values.tolist()
        resources = [[0]*n_r] + resources + [[0]*n_r]
      else:
        resources = [[0]] + [[0]]*n + [[0]]
      if not max_resources:
        max_resources = n_r*[np.inf]
      else:
        max_resources = max_resources
    if not rcpsp_format:
      if 'resources' in df.columns:
        resources = df['resources'].tolist()
        resources = [x.strip().split(",") for x in resources]
        resources = one_hot_resources(resources)
        n_r = len(resources[0])
        resources = [[0]*n_r] + resources + [[0]*n_r]
      if 'resources' not in df.columns:
        resources = [[0]*n_r] + resources + [[0]*n_r]

      if not max_resources:
        max_resources = [1]*n_r
      else:
        max_resources = max_resources

    if 'cost' in df.columns:
      cost = [0] + df['cost'].tolist() + [0]
    else:
      cost = [0] + [0]*n + [0]

    if 'description' in df.columns:
      description = ['Start of Project'] + df['description'].tolist() + ['End of Project']
    else:
      description = ['Start of Project'] + [f'Activity_{x}' for x in activities] + ['End of Project']

    EDGES = []
    for a,prec in zip(activities,precedence):
      if prec == None:
        continue

      for pr in prec:
        if pr == None:
          continue
        EDGES.append((pr,a))

    G = nx.DiGraph()
    G.add_nodes_from(activities)
    G.add_edges_from(EDGES)

    end_prec = []
    for node in activities:
      if node == 'End':
        continue
      if len(nx.descendants(G, node)) == 0:
        G.add_edge(node, 'End')
        end_prec.append(node)
    precedence[-1] = end_prec

    return cls(n_activities = n,n_resources = n_r,activities=activities,
               a_desc = description,a_duration = durations,a_cost = cost,a_precedence = precedence,
               a_resources = resources,max_resources = max_resources,G = G,dummies = True)

  def plot_network_diagram(self,plot_type = 'dot'):

    """
    Generates a network diagram of the project.

    This method visualizes the project's network diagram as a directed graph.
    It first checks if dummy variables have been added and the project network has been created.
    If not, it raises a warning and proceeds to add dummies and create the project network.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    None

    Notes
    -----
    The generated network diagram is saved as 'network_diagram.jpg' in the current directory. It is also displayed as a plot.

    Examples
    --------
    >>> project_instance.plot_network_diagram()
    """

    if not self.dummies_added:
      warnings.warn("!WARNING: Creating dummy variables and creating the project network...")
      self.add_dummies_create_project_network()

    if len(self.PROJECT) == 0:
      warnings.warn("!WARNING: Creating Project data dictionary...")
      self.create_project_dict()

    G = self.graph
    edges = list(G.edges)
    nodes = list(G.nodes)

    if plot_type == 'dot':

      PG = pydot.Dot(graph_type = 'digraph',strict = True,rankdir="LR")
      for i,j in edges:
        edge = pydot.Edge(str(i),str(j))
        PG.add_edge(edge)
      PG.write_png('network_diagram.jpg')
      img = mpimg.imread('network_diagram.jpg')
      plt.figure(figsize=(10,10))
      plt.imshow(img)
      plt.title('Network Diagram')
      plt.axis('off')
      plt.savefig('network_diagram.jpg')
      plt.show()

    if plot_type == 'nx':

      PROJECT = self.PROJECT

      pos = {'Start':(0,0)}
      positions_list = [(0,0)]
      for node in self.PROJECT:
        if node == 'Start':
          continue
        prec = PROJECT[node]['precedence']
        prec_pos = [pos[x] for x in prec]

        x = max([X[0] for X in prec_pos]) + 10
        y = max([Y[1] for Y in prec_pos])

        if (x,y) not in positions_list:
          positions_list.append((x,y))
          pos[node] = (x,y)
        else:
          while (x,y) in positions_list:
            y = y - 5
          positions_list.append((x,y))
          pos[node] = (x,y)

      node_color = ['white'] * len(PROJECT)
      nx.draw(self.graph,pos,with_labels = True,node_size=2000,node_color= node_color, edgecolors='black')
      plt.title('Network Diagram')
      plt.axis('off')
      plt.savefig('network_diagram.jpg')
      plt.show()

  def create_project_dict(self):

    """
    Creates an internal dictionary stored as an instance attribute with all the project relevant data.

    This method generates an internal dictionary that stores project-related information.
    The dictionary is stored as an instance attribute 'PROJECT' and will be used by other methods.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    None

    Notes
    -----
    The dictionary 'PROJECT' is structured as follows:

    .. code-block:: python

        {
            'activity_1': {
                'idx': 0,
                'description': 'Description of activity 1',
                'duration': 5,
                'precedence': [2, 3],
                'resources': ['Resource A', 'Resource B'],
                'cost': 100.0
            },
            'activity_2': {
                'idx': 1,
                'description': 'Description of activity 2',
                'duration': 3,
                'precedence': [],
                'resources': ['Resource C'],
                'cost': 50.0
            },
            # ... More activities ...
        }

    Examples
    --------
    To create the project dictionary, use the following:

    >>> project_instance.create_project_dict()
    """

    if not self.dummies_added:
      warnings.warn("!WARNING: Creating dummy variables and creating the project network...")
      self.add_dummies_create_project_network()

    PROJECT = dict()

    for i,a in enumerate(self.activities):
      inner_dict = {'idx':i,'description':self.a_desc[i],'duration':self.a_duration[i],'precedence':self.a_precedence[i],'resources':self.a_resources[i],'cost':self.a_cost[i]}
      PROJECT[a] = inner_dict
    self.PROJECT = PROJECT

  def CPM(self,verbose=False):

    """
    Runs the Critical Path Method (CPM) scheduling algorithm on the project data and stores its results.
    Calculates relevant information such as immediate successors, total successors, duration of successors, resources of successors, GRPW, etc.
    The results are stored as instance attributes.

    For referesence see:

      - Kelley, James. Critical Path Planning.
      - Santiago, Jesse (February 4, 2009). "Critical Path Method" (PDF).
        Stanford. Archived from the original (PDF) on October 24, 2018. Retrieved October 24, 2018.
      - Kelley, James; Walker, Morgan. Critical-Path Planning and Scheduling. 1959 Proceedings of the Eastern Joint Computer Conference.
      - Kelley, James; Walker, Morgan. The Origins of CPM: A Personal History. PMNETwork 3(2):7–22.
      - Newell, Michael; Grashina, Marina (2003). The Project Management Question and Answer Book. American Management Association. p. 98.
      - Thayer, Harry (1996). Management of the Hanford Engineer Works in World War II, How the Corps, DuPont and the Metallurgical Laboratory fast tracked the original plutonium works. ASCE Press, pp. 66–67.


    Parameters
    ----------
    verbose : bool, optional
        If True, print statements for each step of the algorithm will be displayed. Default is False.

    Returns
    -------
    None

    Raises
    ------
    None

    Notes
    -----
    The method performs both the forward and backward passes of the CPM algorithm,
    calculates the float for each activity, and stores the results in the 'cpm_schedule' attribute.

    Additional attributes:
    - 'cpm_schedule' (dict): A dictionary containing the scheduling results for each activity.
      The structure of each activity's data is as follows:

      .. code-block:: python

          {
              'ES': Early Start,
              'EF': Early Finish,
              'LS': Late Start,
              'LF': Late Finish,
              'F': Float,
              'D': Duration,
              'IS': Immediate Successors,
              'TS': Total Successors,
              'NUM_IS': Number of Immediate Successors,
              'NUM_TS': Number of Total Successors,
              'D_IS': Duration of Immediate Successors,
              'SUM_D_IS': Sum of Duration of Immediate Successors,
              'SUM_RES_IS': Sum of Resources of Immediate Successors,
              'SUM_RES_TS': Sum of Resources of Total Successors,
              'GRPW': Gross Resource and Processing Work
          }

    Examples
    --------
    To run the CPM algorithm with verbose output, use the following:

    >>> project_instance.CPM(verbose=True)
    """

    if len(self.PROJECT) == 0:
      warnings.warn("!WARNING: Creating Project data dictionary...")
      self.create_project_dict()

    PROJECT = self.PROJECT

    CPM_SCHEDULE = dict()

    if verbose:
      print('FORWARD PASS...\n')
    for task in PROJECT:
      if verbose:
        print(f'Current task on the iteration = [{task}]')
      CPM_SCHEDULE[task] = {'ES':0,'EF':0,'LS':0,'LF':0,'F':0,'D':PROJECT[task]['duration'],'IS':None,'TS':None,'NUM_IS':0,'NUM_TS':0}
      prec_constraints = PROJECT[task]['precedence']
      if verbose:
        print(f'The precedence constraints of activity {task} are = {prec_constraints}')
      if prec_constraints == None or prec_constraints =='None':
        if verbose:
          print('The activity is the [Start] so we continue to the next one, since its start and finish are equal to 0')
          print('-'*100)
        continue
      starts = []
      for act in prec_constraints:
        starts.append(CPM_SCHEDULE[act]['EF'])
      if verbose:
        print(f'The finish dates of the precedence constraints of activity [{task}] are = {starts}')
      CPM_SCHEDULE[task]['ES'] = max(starts)
      if verbose:
        print(f"The start date of activity [{task}] is the maximun of the finish dates of its precedence constraints which is equal to ({CPM_SCHEDULE[task]['ES']})")
      CPM_SCHEDULE[task]['EF'] = CPM_SCHEDULE[task]['ES'] + PROJECT[task]['duration']
      if verbose:
        print(f"The finish date of activity [{task}] is then the start:({CPM_SCHEDULE[task]['ES']}) plus the duration:({PROJECT[task]['duration']}) so the finish date is equal to ({CPM_SCHEDULE[task]['EF']})")
        print('-'*100)
      if task == 'End':
        CPM_SCHEDULE[task]['LS'] = CPM_SCHEDULE[task]['ES']
        CPM_SCHEDULE[task]['LF'] = CPM_SCHEDULE[task]['EF']
        if verbose:
          print('For the dummy activity [End] the late finish is equal to the early finish and the late start is equal to the early start ')

    if verbose:
      print('BACKWARD PASS...\n')

    for task in list(PROJECT.keys())[::-1]: # for each activity in the project but going from the end up to the start
      if verbose:
        print(f'Current task on the iteration = [{task}]')
      prec_constraints = PROJECT[task]['precedence'] # get the precedence constraints
      if verbose:
        print(f'The precedence constraints of activity [{task}] are = {prec_constraints}')
      if prec_constraints == None or prec_constraints =='None': # if the precedence constraint is none it means that the activity is the start
        if verbose:
          print('The activity is the [Start] so we continue to the next one, since its start and finish are equal to 0')
          print('-'*100)
        continue
      for act in prec_constraints: # for each activity in the precedence constraint
        if verbose:
          print(f"updating precedence contraint activity [{act}] from data of it's succesor [{task}]")
        if CPM_SCHEDULE[act]['LF'] == 0:
          if verbose:
            print(f'  first time that precedence activity [{act}] is updated in the backward pass')
          CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS'] # the late finish of the precedence c activitis equal to the start of the activity they precede
          if verbose:
            print(f"  precedence activity [{act}] can finish lately on the same date ({CPM_SCHEDULE[act]['LF']}) of the late start ({CPM_SCHEDULE[task]['LS']}) of its succesor [{task}]")
          CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration'] # the late start is equal to late finish minus the duration
          if verbose:
            print(f"  the start of precedence activity [{act}] is then it's finish ({CPM_SCHEDULE[act]['LF']}), minus its duration ({PROJECT[act]['duration']}) which is equal to ({CPM_SCHEDULE[act]['LS']}) ")
        else:
          if verbose:
            print(f'    Attempting to re-update activity [{act}]')
          if CPM_SCHEDULE[task]['LS'] >= CPM_SCHEDULE[act]['LF']:
            if verbose:
              print(f"    The late start of the succesor [{task}] ({CPM_SCHEDULE[task]['LS']}) is bigger than the the current late finish of [{act}] ({CPM_SCHEDULE[act]['LF']}) so no need to update")
            continue
          else:
            if verbose:
              print(f"    precedence activity [{act}] needs an update since its current late finish is bigger than the late start of its succesor")
            CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS']
            if verbose:
              print(f"    precedence activity [{act}] can finish lately on the same date ({CPM_SCHEDULE[act]['LF']}) of the late start ({CPM_SCHEDULE[task]['LS']}) of its succesor [{task}]")
            CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration']
            if verbose:
              print(f"    the start of precedence activity [{act}] is then it's finish ({CPM_SCHEDULE[act]['LF']}), minus its duration ({PROJECT[act]['duration']}) which is equal to {CPM_SCHEDULE[act]['LS']} ")
      CPM_SCHEDULE[task]['F'] = CPM_SCHEDULE[task]['LF'] - CPM_SCHEDULE[task]['EF'] # calculate the float
      if verbose:
        print(f"The float of activity [{task}] is equal to ({CPM_SCHEDULE[task]['F']})")
        print('-'*100)

    EDGES = list(self.graph.edges)

    SUCCESORS = {act:[] for act in PROJECT}
    for n1,n2 in EDGES:
      if n2 != 'End':
        SUCCESORS[n1].append(n2)

    INMEDIATE_SUCCESORS = dict()
    for activity in PROJECT:
      INMEDIATE_SUCCESORS[activity] = len(SUCCESORS[activity])

    DURATION_SUCCESORS = {act:[] for act in PROJECT}
    for n1,n2 in EDGES:
      DURATION_SUCCESORS[n1].append(PROJECT[n2]['duration'])


    RESOURCES_SUCCESORS = {act:[] for act in PROJECT}
    for n1,n2 in EDGES:
      RESOURCES_SUCCESORS[n1].append(sum(PROJECT[n2]['resources']))

    TOTAL_SUCCESORS = {'End':[]}
    for task in list(PROJECT.keys())[::-1]:
      succesor = SUCCESORS[task]
      for act in  succesor:
        succesor = succesor + TOTAL_SUCCESORS[act]
      TOTAL_SUCCESORS[task] = succesor

    RESOURCES_TOTAL_SUCCESORS = {act:[] for act in PROJECT}
    for activity in PROJECT:
      total_succesors_a = set(TOTAL_SUCCESORS[activity])
      total_resources_a = [sum(PROJECT[x]['resources']) for x in total_succesors_a]
      RESOURCES_TOTAL_SUCCESORS[activity] = total_resources_a

    MOST_TOTAL_SUCCESSORS = dict()
    for activity in PROJECT:
      MOST_TOTAL_SUCCESSORS[activity] = len(set(TOTAL_SUCCESORS[activity]))

    for task in CPM_SCHEDULE:

      CPM_SCHEDULE[task]['idx'] = PROJECT[task]['idx']
      CPM_SCHEDULE[task]['IS'] = SUCCESORS[task]
      CPM_SCHEDULE[task]['D_IS'] = DURATION_SUCCESORS[task]
      CPM_SCHEDULE[task]['SUM_D_IS'] = sum(DURATION_SUCCESORS[task])
      CPM_SCHEDULE[task]['SUM_RES_IS'] = sum(RESOURCES_SUCCESORS[task])
      CPM_SCHEDULE[task]['SUM_RES_TS'] = sum(RESOURCES_TOTAL_SUCCESORS[task])
      CPM_SCHEDULE[task]['GRPW'] = CPM_SCHEDULE[task]['SUM_D_IS'] + CPM_SCHEDULE[task]['D']
      CPM_SCHEDULE[task]['TS'] = list(set(TOTAL_SUCCESORS[task]))
      CPM_SCHEDULE[task]['NUM_IS'] = INMEDIATE_SUCCESORS[task]
      CPM_SCHEDULE[task]['NUM_TS'] = MOST_TOTAL_SUCCESSORS[task]

    self.cpm_schedule = CPM_SCHEDULE

    return pd.DataFrame(CPM_SCHEDULE).T.iloc[:,0:6]

  def plot_gantt_cpm(self,early=True,save=False):

    """
    Generates a Gantt chart of the schedule obtained from the Critical Path Method (CPM).

    This method visualizes the project schedule as a Gantt chart, highlighting activities in either their early or late schedule, depending on the 'early' parameter.

    Parameters
    ----------
    early : bool, optional
        If True, the Gantt chart displays the early schedule; otherwise, it displays the late schedule. Default is True.
    save : bool, optional
        If True, saves the Gantt chart as an image file (JPEG). Default is False.

    Returns
    -------
    None

    Raises
    ------
    None

    Notes
    -----
    The Gantt chart represents project activities with bars, and each bar's color indicates the float of the activity:
    - Red bars: Critical activities with zero float.
    - Blue bars (early) or purple bars (late): Non-critical activities with float.

    Examples
    --------
    To generate and display an early schedule Gantt chart, use the following:

    >>> project_instance.plot_gantt_cpm(early=True)

    To generate and display a late schedule Gantt chart, use the following:

    >>> project_instance.plot_gantt_cpm(early=False)

    To save the Gantt chart as an image (e.g., 'EARLY_CPM_GANTT.jpg' or 'LATE_CPM_GANTT.jpg'), use the following:

    >>> project_instance.plot_gantt_cpm(early=True, save=True)
    """

    if len(self.cpm_schedule) == 0:
      warnings.warn("!WARNING: Running critical path method...")
      self.CPM()

    CPM_SCHEDULE = self.cpm_schedule

    y_start = len(CPM_SCHEDULE)-1
    ticks = [y_start - i+0.375 for i in range(1,y_start)][::-1]

    labels = [x for x in CPM_SCHEDULE if x not in ['Start','End']]
    plt.figure(figsize=(14,8))
    title = 'EARLY' if early else 'LATE'
    for i,activity in enumerate(CPM_SCHEDULE):
      if activity in ['Start','End']:
        continue
      if early:
        plt.broken_barh([(CPM_SCHEDULE[activity]['ES'],CPM_SCHEDULE[activity]['D'])],
                        (y_start-i, 0.75),
                        alpha=0.5,color='red' if CPM_SCHEDULE[activity]['F'] == 0 else 'blue',edgecolor='black')
        plt.text(CPM_SCHEDULE[activity]['ES'] + 0.1,
                y_start-i+0.25,
                f'Activity {activity}',fontsize=12)
      else:
        plt.broken_barh([(CPM_SCHEDULE[activity]['LS'],CPM_SCHEDULE[activity]['D'])],
                      (y_start-i, 0.75),
                      alpha=0.5,color='red' if CPM_SCHEDULE[activity]['F'] == 0 else 'purple' ,edgecolor='black')
        plt.text(CPM_SCHEDULE[activity]['LS'] + 0.1,
                y_start-i+0.25,
                f'Activity {activity}',fontsize=12)
    plt.title(f'({title}) Project Schedule', fontsize=12)
    plt.xlabel('Days')
    plt.ylabel('Activities')
    plt.xticks(list(range(CPM_SCHEDULE['End']['LS']+2)),fontsize=12)
    plt.yticks(ticks=ticks,
          labels=labels[::-1], fontsize=12)
    plt.grid()
    if save:
      if early:
        name = 'EARLY_CPM_GANTT.jpg'
      else:
        name = 'LATE_CPM_GANTT.jpg'
      plt.savefig(name)
    plt.show()

  @staticmethod
  def range_overlap(range1, range2):
    """Whether range1 and range2 overlap."""
    x1, x2 = range1.start, range1.stop
    y1, y2 = range2.start, range2.stop
    return x1 < y2 and y1 < x2

  def plot_resource_levels(self,solution = None,max_resources = None):

    """
    Generates a plot that shows the daily resource usage for a given project schedule.

    This method visualizes the daily resource usage based on the provided project schedule and maximum resource limits.

    Parameters
    ----------
    solution : dict, optional
        A dictionary with 'ES' (Early Start) and 'EF' (Early Finish) for each activity of the project. The schedule in question that the user wants to plot.
    max_resources : numpy.ndarray, optional
        Maximum limits for each one of the resources that each activity uses.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If there is no resource data available (n_resources <= 0).

    Notes
    -----
    The resource usage plot displays resource allocation over time, with different resources shown in different colors.
    Resource levels that exceed the maximum limits are highlighted in red.
    Each resource is plotted separately if there are multiple resources, or as a single plot if there is only one resource.

    Examples
    --------
    To generate and display the resource usage plot for a given schedule, use the following:

    >>> project_instance.plot_resource_levels(solution=schedule_data, max_resources=max_resource_limits)

    To generate and display the resource usage plot for the CPM schedule, use the following:

    >>> project_instance.plot_resource_levels()
    """

    if self.n_resources <= 0:
      raise ValueError("No resource data available")

    if len(self.cpm_schedule) == 0:
      warnings.warn("!WARNING: Running critical path method...")
      self.CPM()

    max_resources = max_resources if max_resources is not None else self.max_resources

    if solution is not None:
      resources = self.get_resources(solution)
    if solution is None:
      warnings.warn("!WARNING: Resource level plot for the CPM Schedule")
      resources = self.get_resources()

    capaRessources = max_resources
    colors = ['green', 'darkorange', 'purple', 'red', 'black', 'yellow','blue','brown','pink','tomato','steelblue','blueviolet']*2
    if self.n_resources > 1:

      R,D = resources.shape
      y_lim = resources.max() +1
      figure, axis = plt.subplots(R, 1,figsize=(10, 10))

      for i in range(R):
        for j in range(D):
          axis[i].broken_barh([(j,1)],(0,resources[i,j]),facecolors=colors[i],edgecolor='black')
          axis[i].text(j+0.1,resources[i,j]+ 0.25,f'{resources[i,j]}',bbox=dict(facecolor='red', alpha=0.25))
        axis[i].set_title(f'Resource {i+1}')
        axis[i].axhline( y = capaRessources[i]+0.02, color = 'red',linestyle= 'dashed',lw=4)
        axis[i].set_xticks(range(D+1))
        axis[i].set_ylim(0,y_lim)
      figure.tight_layout()
      figure.subplots_adjust(top=0.95)
      plt.show()

    if self.n_resources == 1:

      plt.figure(figsize=(10, 10))
      R,D = resources.shape
      y_lim = resources.max() +1
      for j in range(D):
        plt.broken_barh([(j,1)],(0,resources[0,j]),facecolors=colors[0],edgecolor='black')
        plt.text(j+0.1,resources[0,j]+ 0.25,f'{resources[0,j]}',bbox=dict(facecolor='red', alpha=0.25))
      plt.axhline( y = capaRessources[0]+0.02, color = 'red',linestyle= 'dashed',lw=4)
      plt.title(f'Resource 1')
      plt.xticks(range(D+1))
      plt.ylim(0,y_lim)
      plt.tight_layout()


  def get_priority_list(self,priority_rule='SPT',verbose=False,save=False):

    """
    Generates a priority list using a heuristic method based on a selected priority rule.

    This method generates a priority list of activities for scheduling based on a selected priority rule.
    The priority rule can be chosen from a set of 24 different options extracted from the literature of the RCPSP.

    For reference, see:

    - "Heuristics for Scheduling Resource-Constrained Projects: An Experimental Investigation," Dale F. Cooper, 1976,
      Management Science, https://doi.org/10.1287/mnsc.22.11.1186
    - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 7)
    - Artigues, Christian, Sophie Demassey, and Emmanuel Neron, eds.
      Resource-constrained project scheduling: models, algorithms, extensions and applications. John Wiley & Sons, 2013. (Chapter 6)
    - Demeulemeester, Erik Leuven, and Willy S. Herroelen. Project scheduling: a research handbook. Vol. 49. Springer Science & Business Media, 2006. (Chapter 6)

    Parameters
    ----------
    priority_rule : str
        The priority rule chosen by the user from the 24 options. Available priority rules include:

        - 'LPT': Longest processing time
        - 'SPT': Shortest processing time
        - 'LIS': Least immediate successors
        - 'MIS': Most immediate successor
        - 'LTS': Least total successors
        - 'MTS': Most total successors
        - 'sEST': Smallest Earliest Start Time
        - 'gEST': Greatest Earliest Start Time
        - 'sEFT': Smallest Earliest Finish Time
        - 'gEFT': Greatest Earliest Finish Time
        - 'sLST': Smallest Latest Start Time
        - 'gLST': Greatest Latest Start Time
        - 'sLFT': Smallest Latest Finish Time
        - 'gLFT': Greatest Latest Finish Time
        - 'MINF': Minimum float
        - 'MAXF': Maximum float
        - 'GRPW': Greatest GRPW
        - 'LRPW': Lowest GRPW
        - 'FCFS': First comes first served
        - 'LCFS': Last comes first served
        - 'GRD': Greatest resource demand
        - 'LRD': Lowest resource demand
        - 'GCRD': Greatest cumulative resource demand
        - 'LCRD': Lowest cumulative resource demand

    verbose : bool, optional
        If True, the user will see each step of the heuristic method. Default is False.
    save : bool, optional
        If True, the priority rule will be stored inside the instance in a list attribute called 'PL'. Default is False.

    Returns
    -------
    PL : list
        Contains the priority list resulted from the heuristic.

    Raises
    ------
    ValueError
        If there is no resource data available (n_resources <= 0).

    Notes
    -----
    The priority list is generated by evaluating activities based on their precedence constraints and the selected
    priority rule. Activities are added to the priority list in the order determined by the priority rule.

    Examples
    --------
    To generate a priority list using the Shortest Processing Time (SPT) rule, use the following:

    >>> project_instance.get_priority_list(priority_rule='SPT')

    To generate a priority list using a different priority rule, such as the Longest Processing Time (LPT) rule, with verbose output and saving the rule:

    >>> project_instance.get_priority_list(priority_rule='LPT', verbose=True, save=True)

    To retrieve the priority list generated for a specific rule, you can access it from the 'PL_list' attribute.
    """

    if self.n_resources <= 0:
      warnings.warn("!WARNING: Priority rules apply when there is a restriction in resources...")

    priority_rules = {'LPT':['D',False], # Longest processing time
                      'SPT':['D',True], # shortest processing time
                      'LIS':['NUM_IS',True], # Least inmediate succesors
                      'MIS':['NUM_IS',False], # Most inmediate succesor
                      'LTS':['NUM_TS',True], # Least total succesors
                      'MTS':['NUM_TS',False], # Most total succesors
                      'sEST':['ES',True], # Smallest Earliest Start Time
                      'gEST':['ES',False], # Greatest Earliest Start Time
                      'sEFT':['EF',True], # Smallest Earliest Finish Time
                      'gEFT':['EF',False], # Greatest Earliest Finish Time
                      'sLST':['LS',True], # Smallest Latest Start Time
                      'gLST':['LS',False], # Greatest Latest Start Time
                      'sLFT':['LF',True], # Smallest Latest Finish Time
                      'gLFT':['LF',False], # Greatest Latest Finish Time
                      'MINF':['F',True], # Minimum float
                      'MAXF':['F',False], # Maximum float
                      'GRPW':['GRPW',False], # Greatest GRPW
                      'LRPW':['GRPW',True],# Greatest GRPW
                      'FCFS':['idx',True], # First comes first served
                      'LCFS':['idx',False], # Last comes first served
                      'GRD':['SUM_RES_IS',False], # Greatest resource demand
                      'LRD':['SUM_RES_IS',True], # lowest resource demand
                      'GCRD':['SUM_RES_TS',False], # Greatest cummulative resource demand
                      'LCRD':['SUM_RES_TS',True],} # lowest cummulative resource demand

    if len(self.cpm_schedule) == 0:
      warnings.warn("!WARNING: Running critical path method...")
      self.CPM()

    PROJECT = self.PROJECT
    extended_CPM_SCHEDULE = self.cpm_schedule

    info , sense = priority_rules[priority_rule]

    if verbose:
      print(f'Generating priority list based on priority rule {priority_rule}\n')
    PL = ['Start']
    unfinished_jobs = [x for x in PROJECT if x not in ['Start','End']]
    while len(unfinished_jobs) > 0:
      to_sche = dict()
      tie = False
      if verbose:
        print(f'Current Priority List = {PL}')
      for task in unfinished_jobs:
        if verbose:
          print(f'  - Current Evaluation of activity ({task})')
          print(f'    * Checking if precedence activities of activity ({task}) are in the priority list')
        #check if the precedent activities are already in the list
        prec_constraints = PROJECT[task]['precedence']
        if verbose:
          print(f'    * Precedence activities of ({task}) = {prec_constraints}')
        valid = 0

        for act in  prec_constraints:
          if act in PL:
            valid += 1
        if valid == len(prec_constraints): # if the activity can be scheduled based on the precedence
          if verbose:
            print(f'    ~ SUCCES: Activity ({task}) is a potential activitiy all its precedents are in the current priority list')
          to_sche[task] = extended_CPM_SCHEDULE[task][info] #then add its duration to the dictionary of potential activities
          continue
        else:
          if verbose:
            print(f'    ~ FAIL: Activity ({task}) cannot be added to the PL, its precedents are NOT in the current priority list')
      to_sche = {k: v for k, v in sorted(to_sche.items(), key=lambda item: item[1],reverse=sense)} # order the dictionary from small to large durations

      if len(to_sche) > 1:
        if list(to_sche.values())[-1] == list(to_sche.values())[-2]: # in case there is a tie
          if verbose:
            print('There is a tie...')
          tie = True
          current_val = list(to_sche.values())[-1] # get the potential activities with the largest values
          to_sche = {k: v for k, v in to_sche.items() if v == current_val} # get the potential activities with the largest values
          to_sche = {k: v for k, v in sorted(to_sche.items(), key=lambda item: item[0],reverse=True)} # order the activities based on their name
      if verbose:
        print(f'potential activities to add to the priority list {to_sche}')
      if not tie:
        a = to_sche.popitem() #remove the activity in the first element
      if tie:
        a2chose = [x for x in to_sche]
        a2chose = sorted(a2chose)[0]
        a = (a2chose,to_sche[a2chose])
      if verbose:
        print(f'Activity {a} ({PROJECT[a[0]]["description"]}) added to the priority list')
        print('-'*150)
      PL.append(a[0])
      unfinished_jobs.remove(a[0])

    PL.append('End')
    if verbose:
      print(f'Priority rule based on rule: {priority_rule} = {PL}')

    if save:
      if not hasattr(self, 'PL_list'):
        self.PL_list = {}
      self.PL_list[priority_rule] = PL

    return PL

  def SSG(self,PL,max_resources = None,verbose=False,save=False):

    """
    Generates a schedule from a priority list using the Serial Scheduling Method for the RCPSP.

    This method generates a schedule for project activities based on a given priority list (PL) and resource constraints.
    The Serial Scheduling Method (SSG) is used to schedule activities in a serial manner, following the order specified in the priority list.

    For reference, see:

    - "Heuristics for Scheduling Resource-Constrained Projects: An Experimental Investigation," Dale F. Cooper, 1976,
      Management Science, https://doi.org/10.1287/mnsc.22.11.1186
    - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 7)
    - Artigues, Christian, Sophie Demassey, and Emmanuel Neron, eds.
      Resource-constrained project scheduling: models, algorithms, extensions and applications. John Wiley & Sons, 2013. (Chapter 6)
    - Demeulemeester, Erik Leuven, and Willy S. Herroelen. Project scheduling: a research handbook. Vol. 49. Springer Science & Business Media, 2006. (Chapter 6)

    Parameters
    ----------
    PL : list
        Priority list to be scheduled.
    max_resources : list, optional
        Resource limit for each of the resources consumed by the project activities. If not provided, the resource limits will be obtained from the instance. Default is None.
    verbose : bool, optional
        If True, the user will see the steps of the scheduling process. Default is False.
    save : bool, optional
        If True, the output schedule will be saved inside the instance. Default is False.

    Returns
    -------
    SSG_SCHEDULE : dict
        A dictionary with each activity as a key. Each key contains an inner dictionary with the 'ES' (Earliest Start) and 'EF' (Earliest Finish) times for the activity.

    Notes
    -----
    The Serial Scheduling Method (SSG) is a simple scheduling algorithm that follows the order of activities in the priority list and schedules them one by one, ensuring resource constraints are met.

    If 'max_resources' is not provided, the resource limits will be obtained from the project instance. If 'save' is set to True, the generated schedule will be stored in the 'SSG_SCHEDULE' attribute for future reference.

    Examples
    --------
    To generate a schedule from a priority list, use the following:

    >>> project_instance.SSG(PL, max_resources=[10, 15, 20], verbose=True, save=True)

    The resulting schedule will be stored in the 'SSG_SCHEDULE' attribute of the project instance.
    """

    if len(self.cpm_schedule) == 0:
      warnings.warn("!WARNING: Running critical path method...")
      self.CPM()

    project = self.PROJECT

    if max_resources is not None:
      max_resources = {f'resource_{i+1}':x for i,x in enumerate(max_resources)}
    if max_resources is None:
      max_resources = {f'resource_{i+1}':x for i,x in enumerate(self.max_resources)}
    #print(max_resources)

    PROJECT = dict()
    for task in project:
      inner = project[task]
      inner_resources = inner['resources']

      inner_resources_dict = {x:y for x,y in zip(list(max_resources.keys()),inner_resources)}

      inner.update(inner_resources_dict)
      PROJECT[task] = inner

    SSG_SCHEDULE = {'Start':{'ES':0,'EF':0}}
    unfinished_jobs = [x for x in PL if x not in ['Start','End']]
    project_finish_date = 0
    planning_horizon = sum([PROJECT[x]['duration'] for x in PROJECT])
    max_resources_list = [max_resources[x] for x in max_resources]

    for task in unfinished_jobs:

      prec_const = PROJECT[task]['precedence']
      precedence_start = [SSG_SCHEDULE[const]['ES'] + PROJECT[const]['duration'] for const in prec_const]
      start_preced = max(precedence_start)
      if verbose:
        print(f'Checking if activity {task} can be scheduled as soon as its predecessors ({prec_const}) are finished on day {start_preced}')
      dur = PROJECT[task]['duration']
      resource_conflicting_activities = [x for x in SSG_SCHEDULE if x != task]
      activities_overlap = []
      if verbose:
        print(f'Checking potential resource conflicting activities being executed between the dates {(start_preced,start_preced+dur)}')
      for a in resource_conflicting_activities:

        r1 = range(start_preced,start_preced+dur)
        r2 = range(SSG_SCHEDULE[a]['ES'],SSG_SCHEDULE[a]['EF'])

        if self.range_overlap(r1,r2):
          activities_overlap.append(a)
      if verbose:
        print(f'The following activites: {activities_overlap} have a potential conflict with activity {task}')
        print(f'Checking total daily resources between the dates {((start_preced,start_preced+dur))}')
      res_per_day = []
      for day in range(start_preced,start_preced + dur+1):
        resources_per_activity = {x:PROJECT[task][x] for x in max_resources} # dictionary of all resources initialized to the value of the task in question
        for a2 in activities_overlap:

          r3 = range(day,day+1)
          r4 = range(SSG_SCHEDULE[a2]['ES'],SSG_SCHEDULE[a2]['EF'])
          if self.range_overlap(r3,r4):

            for res in resources_per_activity:
              resources_per_activity[res] += PROJECT[a2][res]

        res_day_a2 = [resources_per_activity[res] for res in resources_per_activity]
        res_per_day.append((day,res_day_a2))
      if verbose:
        print(f'Resources per day = {res_per_day}')
      is_valid = True
      for day,res in res_per_day:
        clause = np.array(res) > max_resources_list
        clause = clause.sum()
        if clause > 0:
          is_valid = False
          break
      if is_valid:
        SSG_SCHEDULE[task] =  {'ES':start_preced,'EF':start_preced + dur}
        if SSG_SCHEDULE[task]['EF'] > project_finish_date:
          project_finish_date = SSG_SCHEDULE[task]['EF']
        if verbose:
          print(f'Activity {task} ({PROJECT[task]["description"]}) can be scheduled just after its succesors on day {start_preced} finishing on date {start_preced+dur} and maxmimum resource limits are not exceeded')
          print('-'*100)
        continue


      resource_conflicting_activities = [x for x in SSG_SCHEDULE if x != task ]
      resource_conflicting_activities = [x for x in resource_conflicting_activities if SSG_SCHEDULE[x]['EF'] >= start_preced]
      valid_dates = []
      potential_dates = [SSG_SCHEDULE[x]['ES'] for x in resource_conflicting_activities]
      potential_dates = potential_dates + [SSG_SCHEDULE[x]['EF'] for x in resource_conflicting_activities]
      potential_dates = [x for x in potential_dates if x > start_preced]
      potential_dates = list(set(potential_dates))
      potential_dates.sort()
      date_to_beat = planning_horizon
      if verbose:
        print(f'Activity {task} could NOT be scheduled just after its succesors, checking other potential dates {potential_dates}')

      for date in potential_dates:

        if date >= date_to_beat:
          continue

        activities_overlap = []
        for a in resource_conflicting_activities:

          r1 = range(date,date+dur)
          r2 = range(SSG_SCHEDULE[a]['ES'],SSG_SCHEDULE[a]['EF'])

          if self.range_overlap(r1,r2):
            activities_overlap.append(a)
        res_per_day = []
        for day in range(date,date+dur+1):
          resources_per_activity = {x:PROJECT[task][x] for x in max_resources}
          for a2 in activities_overlap:

            r3 = range(day,day+1)
            r4 = range(SSG_SCHEDULE[a2]['ES'],SSG_SCHEDULE[a2]['EF'])
            if self.range_overlap(r3,r4):

              for res in resources_per_activity:
                resources_per_activity[res] += PROJECT[a2][res]

          res_day_a2 = [resources_per_activity[res] for res in resources_per_activity]
          res_per_day.append((day,res_day_a2))

        is_valid = True
        for day,res in res_per_day:
          clause = np.array(res) > max_resources_list
          clause = clause.sum()
          if clause > 0:
            is_valid = False
            break
        if is_valid:
          valid_dates.append(date)
          date_to_beat = date

      final_date = min(valid_dates)
      if verbose:
        print(f'Dates to schedule on which maxmimum resource limits are not exceeded {valid_dates}')
        print(f'Activity {task} {({PROJECT[task]["description"]})} was scheduled to start on date {final_date} and it will finish on date {final_date+dur}')
        print('-'*100)
      SSG_SCHEDULE[task] =  {'ES':final_date,'EF':final_date + dur}
      if SSG_SCHEDULE[task]['EF'] > project_finish_date:
          project_finish_date = SSG_SCHEDULE[task]['EF']

    SSG_SCHEDULE['End'] =  {'ES':project_finish_date,'EF':project_finish_date}

    if save:
      self.SSG = SSG_SCHEDULE

    return SSG_SCHEDULE

  @staticmethod
  def check_activity_day_schedulable(date,activity,PROJECT,PSG_SCHEDULE,max_resources,verbose=False):

    def range_overlap(range1, range2):
      """Whether range1 and range2 overlap."""
      x1, x2 = range1.start, range1.stop
      y1, y2 = range2.start, range2.stop
      return x1 < y2 and y1 < x2

    max_resources_list = [max_resources[x] for x in max_resources]

    prec_const = PROJECT[activity]['precedence']
    #print(prec_const)
    valid = 0
    for act in  prec_const:
      if act in PSG_SCHEDULE:
        valid += 1
    #print(valid,len(prec_const))
    if valid == len(prec_const):
      precedence_start = [PSG_SCHEDULE[const]['ES'] + PROJECT[const]['duration'] for const in prec_const]
      start_preced = max(precedence_start)
      if date < start_preced:
        if verbose:
          print(f'  Current activities in Schedule = {PSG_SCHEDULE}')
          print(f'  FAIL: The date ({date}) demanded to start {activity} is less than the finish dates of the precedence constraint activities {prec_const}')
          #print('-'*50)
        return False

      dur = PROJECT[activity]['duration']
      resource_conflicting_activities = [x for x in PSG_SCHEDULE if x != activity]
      resources_per_activity = {x:PROJECT[activity][x] for x in max_resources}

      if verbose:
        print(f'  Checking potential conflicting activities on date range {(date,date+dur)}')

      activities_overlap = []
      r1 = range(date,date+dur)
      for a1 in resource_conflicting_activities:
        r2 = range(PSG_SCHEDULE[a1]['ES'],PSG_SCHEDULE[a1]['EF'])
        if range_overlap(r1,r2):
          activities_overlap.append(a1)
      if verbose:
        print(f'    Potential resource conflicting activities = {activities_overlap}')
      if len(activities_overlap)==0:
        #print('No conflicting activities')
        #print('-'*50)
        return True
      res_per_day = []
      for day in range(date,date+dur+1):
        resources_per_activity = {x:PROJECT[activity][x] for x in max_resources}
        for a2 in activities_overlap:
          r3 = range(day,day+1)
          r4 = range(PSG_SCHEDULE[a2]['ES'],PSG_SCHEDULE[a2]['EF'])
          if range_overlap(r3,r4):
            for res in resources_per_activity:
              resources_per_activity[res] += PROJECT[a2][res]
        res_day_a2 = [resources_per_activity[res] for res in resources_per_activity]
        res_per_day.append((day,res_day_a2))
      if verbose:
        print(f'    Resources per day = {res_per_day}')

      is_valid = True
      for day,res in res_per_day:
        clause = np.array(res) > max_resources_list
        clause = clause.sum()
        if clause > 0:
          is_valid = False
          break
      if is_valid:
        #print(res_per_day,clause)
        if verbose:
          print(f'    SUCCESS: Activity {activity} not exceeding maximum resource limits between the date range {(date,date+dur)}')
        #print('-'*50)
        return True
      else:
        #print(res_per_day,clause)
        if verbose:
          print(f'    FAIL: Activity {activity} violates maximum resource limits between the specified date range {(date,date+dur)}')
        #print('-'*50)
        return False
    else:
      if verbose:
        print(f'  Current activities in Schedule = {list(PSG_SCHEDULE.keys())}')
        print(f'  FAIL: Precedence constraint activities of activity {activity} ({prec_const}) are not in the schedule')
        #print('-'*50)
      return False

  def PSG(self,PL,max_resources = None,verbose=False,save=False):

    """
    Generates a schedule from a priority list using the Parallel Scheduling Generation Method for the RCPSP.

    This method generates a schedule for project activities based on a given priority list (PL) and resource constraints.
    The Parallel Scheduling Generation Method (PSG) is used to schedule activities in parallel whenever possible, allowing activities with no resource conflicts to start concurrently.

    For reference, see:

    - "Heuristics for Scheduling Resource-Constrained Projects: An Experimental Investigation," Dale F. Cooper, 1976,
      Management Science, https://doi.org/10.1287/mnsc.22.11.1186
    - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 7)
    - Artigues, Christian, Sophie Demassey, and Emmanuel Neron, eds.
      Resource-constrained project scheduling: models, algorithms, extensions and applications. John Wiley & Sons, 2013. (Chapter 6)
    - Demeulemeester, Erik Leuven, and Willy S. Herroelen. Project scheduling: a research handbook. Vol. 49. Springer Science & Business Media, 2006. (Chapter 6)

    Parameters
    ----------
    PL : list
        Priority list to be scheduled.
    max_resources : list, optional
        Resource limit for each of the resources consumed by the project activities. If not provided, the resource limits will be obtained from the instance. Default is None.
    verbose : bool, optional
        If True, the user will see the steps of the scheduling process. Default is False.
    save : bool, optional
        If True, the output schedule will be saved inside the instance. Default is False.

    Returns
    -------
    PSG_SCHEDULE : dict
        A dictionary with each activity as a key. Each key contains an inner dictionary with the 'ES' (Earliest Start) and 'EF' (Earliest Finish) times for the activity.

    Notes
    -----
    The Parallel Scheduling Generation Method (PSG) is an advanced scheduling algorithm that allows activities to be scheduled in parallel whenever possible, optimizing resource utilization and project completion time.

    If 'max_resources' is not provided, the resource limits will be obtained from the project instance. If 'save' is set to True, the generated schedule will be stored in the 'PSG_SCHEDULE' attribute for future reference.

    Examples
    --------
    To generate a schedule from a priority list, use the following:

    >>> project_instance.PSG(PL, max_resources=[10, 15, 20], verbose=True, save=True)

    The resulting schedule will be stored in the 'PSG_SCHEDULE' attribute of the project instance.
    """

    """
    Generates a schedule from a priority list using the Parallel Scheduling Generation Method for the RCPSP.

    This method generates a schedule for project activities based on a given priority list (PL) and resource constraints.
    The Parallel Scheduling Generation Method (PSG) is used to schedule activities in parallel whenever possible,
    allowing activities with no resource conflicts to start concurrently.

    Inputs:
    - PL (list): Priority list to be scheduled.
    - max_resources (list): Resource limit for each of the resources consumed by the project activities. If not provided,
      the resource limits will be obtained from the instance.
    - verbose (bool): If True, the user will see the steps of the scheduling process.
    - save (bool): If True, the output schedule will be saved inside the instance.

    Outputs:
    PSG_SCHEDULE (dict): A dictionary with each activity as a key. Each key contains an inner dictionary with the
    'ES' (Earliest Start) and 'EF' (Earliest Finish) times for the activity.

    Usage:
    To generate a schedule from a priority list:
    project_instance.PSG(PL, max_resources=[10, 15, 20], verbose=True, save=True)

    The resulting schedule will be stored in the 'PSG_SCHEDULE' attribute of the project instance.

    The Parallel Scheduling Generation Method (PSG) is an advanced scheduling algorithm that allows activities to be
    scheduled in parallel whenever possible, optimizing resource utilization and project completion time.

    If 'max_resources' is not provided, the resource limits will be obtained from the project instance. If 'save' is set
    to True, the generated schedule will be stored in the 'PSG_SCHEDULE' attribute for future reference.

    """

    if len(self.cpm_schedule) == 0:
      warnings.warn("!WARNING: Running critical path method...")
      self.CPM()

    project = self.PROJECT

    if max_resources is not None:
      max_resources = {f'resource_{i+1}':x for i,x in enumerate(max_resources)}
    if max_resources is None:
      max_resources = {f'resource_{i+1}':x for i,x in enumerate(self.max_resources)}
    #print(max_resources)

    PROJECT = dict()
    for task in project:
      inner = project[task]
      inner_resources = inner['resources']

      inner_resources_dict = {x:y for x,y in zip(list(max_resources.keys()),inner_resources)}

      inner.update(inner_resources_dict)
      PROJECT[task] = inner

    planning_horizon = sum(self.a_duration)
    PSG_SCHEDULE = {'Start':{'ES':0,'EF':0}}
    unfinished_jobs = [x for x in PL if x not in ['Start','End']]
    Scheduled = []
    project_finish_date = 0

    for day in range(planning_horizon):
      if len(Scheduled) == len(unfinished_jobs):
        break

      for activity in unfinished_jobs:
        if activity in Scheduled:
            continue
        if verbose:
          print(f'Attempting to schedule activity {activity} on day {day}')
        if self.check_activity_day_schedulable(day,activity, PROJECT,PSG_SCHEDULE,max_resources,verbose):
          dur = PROJECT[activity]['duration']
          PSG_SCHEDULE[activity] = {'ES':day,'EF':day + dur}
          if verbose:
            print(f'  SUCCESS: Activity {activity} ({PROJECT[activity]["description"]}) succesfully scheduled on day {day}, finishing on date {day + dur}')
            #print('-'*150)
          if PSG_SCHEDULE[activity]['EF'] > project_finish_date:
            project_finish_date = PSG_SCHEDULE[activity]['EF']
          Scheduled.append(activity)
      if verbose:
        print()
        print('*'*150)
        print()
    PSG_SCHEDULE['End'] =  {'ES':project_finish_date,'EF':project_finish_date}

    SCHEDULE_OUT = {'Start':{'ES':0,'EF':0}}
    for a in unfinished_jobs:
      SCHEDULE_OUT[a] = PSG_SCHEDULE[a]
    SCHEDULE_OUT['End'] = PSG_SCHEDULE['End']

    if save:
      self.PSG = SCHEDULE_OUT

    return SCHEDULE_OUT

  # no necesariamente tiene que estar adentro de la clase

  def get_individual_resources(self,solution,resource_id = 0):

    """
    Returns the daily consumption of a specific resource for the entire project horizon/makespan.

    Given a schedule and a specific resource, this method calculates the daily consumption of the resource over the entire project horizon or makespan.

    Parameters
    ----------
    solution : dict
        A dictionary with the activities as keys,
        and each key has an inner dictionary with the 'ES' (Earliest Start) and 'EF' (Earliest Finish) of each activity in the schedule.
        Example: {'A': {'ES': 5, 'EF': 10}, 'B': {'ES': 8, 'EF': 12}, ...}
    resource_id : int, optional
        An integer that refers to the resource of interest to evaluate. Default is 0.

    Returns
    -------
    resource_horizon : numpy.ndarray
        An array representing the daily consumption of the specified resource over the project horizon/makespan.
        Each element of the array corresponds to a day, and the value at each day represents the cumulative consumption of the resource up to that day.

    Notes
    -----
    The 'resource_horizon' array provides a day-by-day view of the resource consumption throughout the project's execution.

    Examples
    --------
    To calculate the daily consumption of resource 0 for a given schedule, use the following:

    >>> resource_consumption = project_instance.get_individual_resources(schedule, resource_id=0)
    """

    PROJECT = self.PROJECT
    ph = solution['End']['EF'] + 1
    resource_horizon = np.zeros(ph,dtype = int)

    for a in PROJECT:

      if a in ['Start','End']:
        continue

      a_res = PROJECT[a]['resources'][resource_id]
      if a_res == 0:
        continue

      x_start = solution[a]['ES']
      x_finish = solution[a]['EF']

      y_start = resource_horizon[x_start:x_finish].max()
      y_finish = y_start + a_res

      for i in range(x_start,x_finish):
         resource_horizon[i] = y_finish

    return resource_horizon

  def get_resources(self,solution = None):

    """
    Returns the daily consumption of all resources used by the project for the entire project horizon/makespan.

    Given a schedule and resource information for the project, this method calculates the daily consumption of each resource over the entire project horizon or makespan.

    Parameters
    ----------
    solution : dict, optional
        A dictionary with the activities as keys, and each key has an inner dictionary with the 'ES' (Earliest Start) and 'EF' (Earliest Finish) of each activity in the schedule. Example: {'A': {'ES': 5, 'EF': 10}, 'B': {'ES': 8, 'EF': 12}, ...} If not provided, the method will use the schedule obtained from the Critical Path Method (CPM).

    Returns
    -------
    resources : numpy.ndarray
        A 2D array representing the daily consumption of each resource used by the project. Each row corresponds to a resource, and each column represents a day. The values in the array indicate the cumulative consumption of each resource up to each day.

    Notes
    -----
    The 'resources' array provides a day-by-day view of the resource consumption for each resource throughout the project's execution.

    Examples
    --------
    To calculate the daily consumption of all resources for a given schedule, use the following:

    >>> resource_consumption = project_instance.get_resources(schedule)

    The resulting 'resource_consumption' array provides a day-by-day view of the resource consumption for each resource throughout the project's execution.
    """

    if self.n_resources <= 0:
      raise ValueError("No resource data available")

    if len(self.cpm_schedule) == 0:
      warnings.warn("!WARNING: Running critical path method...")
      self.CPM()

    activityRessourceConsumption = self.a_resources
    if solution == None:
      solution = self.cpm_schedule

    ph = solution['End']['EF'] +1
    n_r = self.n_resources
    resources = np.zeros((n_r,ph),dtype = int)
    for i in range(n_r):
      resources[i] = self.get_individual_resources(solution,resource_id = i)

    return resources


  def RCPSP_plot(self,solution,resource_id = 0,max_resources = None):

    """
    Creates an RCPSP plot for a given resource.

    This function generates a timeline plot for each activity that consumes the specified resource.
    Each activity is represented as a box on the timeline.
    The x-axis corresponds to the activity's "start" and "end" dates, while the y-axis represents the resource usage level for each date within the activity's duration.

    Parameters:
    ----------
    self : object
        The project instance to which this function belongs.
    solution : dict
        A Schedule dictionary that contains each activity name as keys, with inner dictionaries specifying the "ES" (Early Start) and "EF" (Early Finish) of each activity.
        Example: {'A': {'ES': 5, 'EF': 10}}.
    resource_id : int, optional
        The integer representing the resource of interest that the user wants to visualize. Default is 0.
    max_resources : list, optional
        A list containing the resource limits for each resource consumed by the project. If not provided, it uses the maximum resources from the project instance.

    Returns:
    -------
    None

    Notes:
    -----
    This function creates a timeline plot for activities that consume the specified resource. It visualizes the resource usage over time for the selected resource.

    Examples:
    --------
    To generate an RCPSP plot for resource 0 using a provided solution and resource limits:

    >>> project_instance.RCPSP_plot(solution=schedule, resource_id=0, max_resources=resource_limits)

    This will display the RCPSP plot for resource 0 based on the provided solution and resource limits.
    """

    PROJECT = self.PROJECT
    ph = solution['End']['EF'] + 1
    resource_horizon = np.zeros(ph,dtype = int)
    colors = ['green', 'darkorange', 'purple', 'red', 'black', 'yellow','blue','brown','pink','tomato','steelblue','blueviolet']*2
    max_resources = max_resources if max_resources is not None else self.max_resources
    coordinates = dict()

    for a in PROJECT:

      if a in ['Start','End']:
        continue

      a_res = PROJECT[a]['resources'][resource_id]
      if a_res == 0:
        continue

      x_start = solution[a]['ES']
      x_finish = solution[a]['EF']


      y_start = resource_horizon[x_start:x_finish].max()
      y_finish = y_start + a_res

      coordinates[a] = {'X0':x_start,'X1':x_finish,'Y0':y_start,'Y1':y_finish}
      for i in range(x_start,x_finish):
         resource_horizon[i] = y_finish

    plt.figure(figsize=(10, 6))
    for x in coordinates:

      x_diff = coordinates[x]['X1'] - coordinates[x]['X0']
      y_diff = coordinates[x]['Y1'] - coordinates[x]['Y0']

      plt.broken_barh([(coordinates[x]['X0'],x_diff)],(coordinates[x]['Y0'],y_diff),facecolors=colors[resource_id],edgecolor='black',alpha=0.5)
      plt.text(coordinates[x]['X0']+0.5,coordinates[x]['Y0']+ 0.25,f'{x}',bbox=dict(facecolor='red', alpha=1))

    y_lim = resource_horizon.max() + 1
    plt.axhline( y = max_resources[resource_id]+0.02, color = 'red',linestyle= 'dashed',lw=4)
    plt.xticks(range(0,ph+1))
    plt.title(f'Resource {resource_id+1}')
    plt.ylim(0,y_lim)
    plt.tight_layout()
    plt.show()

  def get_critical_path(self):

    """
    Returns the activities on the critical path obtained from the Critical Path Scheduling method.

    The critical path represents the sequence of activities with zero float, meaning that any delay in these activities would directly impact the project's completion time.

    For referesence see:

      - Kelley, James. Critical Path Planning.
      - Santiago, Jesse (February 4, 2009). "Critical Path Method" (PDF).
        Stanford. Archived from the original (PDF) on October 24, 2018. Retrieved October 24, 2018.
      - Kelley, James; Walker, Morgan. Critical-Path Planning and Scheduling. 1959 Proceedings of the Eastern Joint Computer Conference.
      - Kelley, James; Walker, Morgan. The Origins of CPM: A Personal History. PMNETwork 3(2):7–22.
      - Newell, Michael; Grashina, Marina (2003). The Project Management Question and Answer Book. American Management Association. p. 98.
      - Thayer, Harry (1996). Management of the Hanford Engineer Works in World War II, How the Corps, DuPont and the Metallurgical Laboratory fast tracked the original plutonium works. ASCE Press, pp. 66–67.

    Parameters
    ----------
    None

    Returns
    -------
    CP : list
        A list containing the activity names of the activities on the critical path.

    Notes
    -----
    The 'CP' list contains the names of the activities that constitute the critical path in the project schedule.

    Examples
    --------
    To obtain the activities on the critical path, use the following:

    >>> critical_path_activities = project_instance.get_critical_path()

    The resulting 'critical_path_activities' list contains the names of the activities that constitute the critical path in the project schedule.
    """

    if len(self.cpm_schedule) == 0:
      warnings.warn("!WARNING: Running critical path method...")
      self.CPM()

    CPM_SCHEDULE = self.cpm_schedule
    CP = []
    for activity in CPM_SCHEDULE:
      if CPM_SCHEDULE[activity]['F'] == 0:
        CP.append(activity)
    return CP

  def get_critical_chain(self,solution = None,max_resources = None):

    """
    Returns a list of activities that form the critical chain in a project schedule with resource constraints.

    The critical chain consists of activities that, if delayed by even one day, would either extend the project's makespan or violate one or more resource constraints.

    For reference see:
      - Goldratt, Eliyahu M. Critical chain: A business novel. Routledge, 2017.
      - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 10)
      - Herroelen, Willy, Roel Leus, and Erik Demeulemeester. "Critical chain project scheduling: Do not oversimplify." Project Management Journal 33.4 (2002): 48-60.

    Parameters
    ----------
    solution : dict
        A dictionary representing the project schedule with activity start ('ES') and finish ('EF') times. Example: {'A': {'ES': 5, 'EF': 10}}.
    max_resources : list
        A list containing the maximum limits for each resource used by the project.

    Returns
    -------
    critical_chain : list
        A list of activity names that are part of the critical chain.

    Notes
    -----
    The 'critical_chain' list contains the names of activities that are part of the critical chain based on the provided schedule and resource constraints.

    Examples
    --------
    To obtain the critical chain activities, use the following:

    >>> critical_chain_activities = project_instance.get_critical_chain(solution=schedule, max_resources=resource_limits)

    The 'critical_chain_activities' list contains the names of activities that are part of the critical chain based on the provided schedule and resource constraints.
    """

    if len(self.cpm_schedule) == 0:
      warnings.warn("!WARNING: Running critical path method...")
      self.CPM()

    if max_resources is None:
      max_resources = self.max_resources

    if len(max_resources) != self.n_resources:
      raise ValueError(f'Number of resoures in max_resources array not valid and different from the number of resources registered in the problem data ({self.n_resources})')

    critical_chain = []
    CPM_SCHEDULE = self.cpm_schedule
    PROJECT = self.PROJECT

    for a in solution:

      if a in ['Start','End']:
        continue
      IS = CPM_SCHEDULE[a]['IS']
      if len(IS) == 0:
        IS = ['End']
      start_ES_IS = [solution[x]['ES'] for x in IS]
      EF_test = solution[a]['EF'] + 1

      cond = EF_test > np.array(start_ES_IS)
      if np.sum(cond) > 0:
        critical_chain.append(a)
        continue

      test_solution = copy.deepcopy(solution)
      test_solution[a]['EF'] = EF_test
      max_res_sol = np.max(self.get_resources(test_solution),axis = 1)

      res_cond = max_res_sol <= np.array(max_resources)
      if np.sum(res_cond) != self.n_resources:
        critical_chain.append(a)
        continue
    return critical_chain

  # no necesariamente tiene que estar adentro de la clase
  def generate_datetime_schedule(self,solution = None,start_date = None,date_format = '%Y-%m-%d',weekends_work = False,max_resources = None,verbose=False,save=False):

    """
    Transform a given schedule into a datetime schedule, considering weekends and resource constraints.

    This method takes a project schedule, a start date, and other optional parameters to generate a datetime-based schedule.
    It handles weekends as non-working days and ensures that activities do not start or finish on weekends.
    If weekends are working days, the schedule is adjusted accordingly.

    Parameters:
    ----------
    self : object
        The project instance to which this method belongs.
    solution : dict
        A Schedule dictionary that contains each activity name as keys, with inner dictionaries specifying the "ES" (Early Start) and "EF" (Early Finish) of each activity.
        Example: {'A': {'ES': 5, 'EF': 10}}.
    start_date : datetime object or str, optional
        The start date for the project. If not provided, it defaults to the current date.
    date_format : str, optional
        The date format to use when parsing the start date if it is provided as a string. Default is '%Y-%m-%d'.
        The method will try multiple date formats before raising an error:
          * '%Y-%m-%d'
          * '%Y-%d-%m'
          * '%d-%m-%Y'
          * '%m-%d-%Y'
          * '%m/%d/%Y'
          * '%d/%m/%Y'
    weekends_work : bool, optional
        If True, weekends are considered working days, and no adjustments are made for weekends. If False (default), weekends are considered non-working days, and the schedule is adjusted accordingly.
    max_resources : list, optional
        A list containing the resource limits for each resource consumed by the project. If not provided, it uses the maximum resources from the project instance.
    verbose : bool, optional
        If True, the method provides detailed information about the steps taken to adapt the schedule to dates and weekend characteristics. Default is False.
    save : bool, optional
        If True, the output DataFrame will be saved inside the instance as an attribute self.SCHEDULE_DF. Default is False.

    Returns:
    -------
    SCHEDULE_DF : DataFrame
        A DataFrame with the start date, end date, and other relevant information for each activity of the project.

    Notes:
    -----
    This method transforms the project schedule into a datetime schedule, considering weekends and resource constraints. It can be used to analyze project timelines while accounting for non-working days.

    Examples:
    --------
    To generate a datetime schedule with non-working weekends:

    >>> project_instance.generate_datetime_schedule(solution=schedule, start_date='2023-09-01', weekends_work=False, verbose=True)

    This will generate a datetime-based schedule, considering non-working weekends, and provide detailed information if the verbose flag is set to True.
    """

    def is_weekend(day):
    # Check if the day is a Saturday or Sunday (weekday() returns 5 for Saturday and 6 for Sunday)
      return day.weekday() >= 5

    def count_weekend_days_in_date_range(start_date, end_date):
      current_date = start_date
      weekend_days_count = 0
      while current_date <= end_date:
          if is_weekend(current_date):
              weekend_days_count += 1
          current_date += datetime.timedelta(days=1)
      return weekend_days_count

    def return_schedule_with_weekends(solution,verbose=False):

      for a in solution:

        if a == 'Start' or  a == 'End':
          continue

        count = 0
        while is_weekend(solution[a]['ES_date']):
          solution[a]['ES_date'] = solution[a]['ES_date'] + datetime.timedelta(1)
          solution[a]['EF_date'] = solution[a]['EF_date'] + datetime.timedelta(1)
          count += 1

        if verbose:
          print(f"start date of activity {a} shifted by {count} days to avoid starting on a weekend")

        s = solution[a]['ES_date']
        f = solution[a]['EF_date']

        if verbose:
          print('Start date day:', s.strftime('%A'))
          print(f"Duration = {solution[a]['EF'] - solution[a]['ES']}")
          print('Finish date day:', f.strftime('%A'))

        EF = solution[a]['EF']

        weed = count_weekend_days_in_date_range(s, f)

        new_f = f + datetime.timedelta(weed)

        end_count = 0
        while is_weekend(new_f):

          new_f += datetime.timedelta(1)
          end_count += 1

        solution[a]['EF_date'] = new_f
        if verbose:
          print(f"End date of activity:{a}, moved by {weed + end_count} days from {f} to {new_f}")

        succs = [x for x in solution if solution[x]['ES'] == EF if x != a]

        if verbose:
          print(f"succesors of {a} = {succs}")

        for suc in succs:
          s_suc = solution[a]['ES_date']

          if s_suc < new_f:
            dur = solution[suc]['EF'] - solution[suc]['ES']

            solution[suc]['ES_date'] = new_f
            solution[suc]['EF_date'] = new_f + datetime.timedelta(dur)
            if verbose:
              print(f"start of Succesor:{suc} shifted from {s_suc} to {new_f}")
        if verbose:
          print("-"*100)

      return solution

    if solution is None:
      SCHEDULE = self.cpm_schedule
    if solution is not None:
      SCHEDULE = solution
    if start_date == None:
      start_date = datetime.date.today()

    if isinstance(start_date,datetime.date):
      start_date = start_date

    if max_resources is None:
      max_resources = self.max_resources

    if isinstance(start_date,str):
      try:
        warnings.warn("!WARNING: Trying date format (%Y-%m-%d) ...")
        start_date = datetime.datetime.strptime(start_date, date_format)
      except:
        try:
          warnings.warn("!WARNING: Trying date format (%Y-%d-%m) ...")
          date_format_t = '%Y-%d-%m'
          start_date = datetime.datetime.strptime(start_date,date_format_t)
        except:
          try:
            warnings.warn("!WARNING: Trying date format (%d-%m-%Y) ...")
            date_format_t = '%d-%m-%Y'
            start_date = datetime.datetime.strptime(start_date,date_format_t)
          except:
            try:
              warnings.warn("!WARNING: Trying date format (%m-%d-%Y) ...")
              date_format_t = '%m-%d-%Y'
              start_date = datetime.datetime.strptime(start_date,date_format_t)
            except:
              try:
                warnings.warn("!WARNING: Trying date format (%m/%d/%Y) ...")
                date_format_t = '%m/%d/%Y'
                start_date = datetime.datetime.strptime(start_date,date_format_t)
              except:
                try:
                  warnings.warn("!WARNING: Trying date format (%d/%m/%Y) ...")
                  date_format_t = '%d/%m/%Y'
                  start_date = datetime.datetime.strptime(start_date,date_format_t)
                except:
                  raise ValueError(f'Sorry date:{start_date} with format {date_format} not recognized, please input valid date format pair. Or proceed to input a datetime object')


    for a in SCHEDULE:

        SCHEDULE[a]['ES_date'] = start_date + datetime.timedelta(SCHEDULE[a]['ES'])
        SCHEDULE[a]['EF_date'] = start_date + datetime.timedelta(SCHEDULE[a]['EF'])

    if weekends_work:
      if verbose:
        SCHEDULE = return_schedule_with_weekends(SCHEDULE,verbose=verbose)
      # if not verbose:
      #   SCHEDULE = return_schedule_with_weekends(SCHEDULE)

    if solution is None:
      CP = self.get_critical_path()
    if solution is not None:
      CP = self.get_critical_chain(solution = solution,max_resources = max_resources)

    crit = {x:True if x in CP else False for x in SCHEDULE}

    DF = pd.DataFrame(SCHEDULE).T
    DF['D'] = DF['EF'] - DF['ES']
    DF['EF_date'] = pd.to_datetime(DF['EF_date'])
    DF['ES_date'] = pd.to_datetime(DF['ES_date'])
    DF['ES_weekday'] = DF['ES_date'].dt.day_name()
    DF['EF_weekday'] = DF['EF_date'].dt.day_name()
    DF['calendar_duration'] = (DF['EF_date'] - DF['ES_date']).dt.days
    DF['precedence'] = {y:",".join(x) if x is not None else '' for y,x in zip(self.activities,self.a_precedence)}
    DF['critical'] = crit

    columns = ['D','precedence','ES','EF','ES_date','EF_date','ES_weekday','EF_weekday','calendar_duration','critical']
    DF = DF[columns]

    if verbose:
      print(f"Project Schedule duration ({DF.loc['End','EF'] - DF.loc['Start','ES']})")
      print(f"Project Calendar duration ({DF.loc['End','EF_date'] - DF.loc['Start','ES_date']})")

    if save:

      self.SCHEDULE_DF = DF

    return DF

  def plot_date_gantt(self,solution,plot_type = 'plotly'):

    """
    Generate an interactive Gantt chart plot using Plotly.

    This method takes a project schedule in DataFrame format, including start dates and end dates for each activity, and generates an interactive Gantt chart plot using Plotly.
    The Gantt chart provides a visual representation of the project schedule, including critical activities and weekend dates.

    Parameters:
    ----------
    self : object
        The project instance to which this method belongs.
    solution : DataFrame
        A DataFrame containing the project schedule with columns "ES_date" (Early Start Date) and "EF_date" (Early Finish Date) for each activity.
        If not provided as a valid DataFrame, it attempts to generate it using the generate_datetime_schedule method.

    Returns:
    -------
    None

    Notes:
    -----
    This method creates an interactive Gantt chart plot to visualize the project schedule.
    It uses Plotly to generate the plot, allowing for zooming, panning, and interactive exploration of the project timeline.
    If the provided solution is not a valid DataFrame, it attempts to generate it using the generate_datetime_schedule method.
    It will raise an error in case the valid DataFrame cannot be generated

    Examples:
    --------
    To generate an interactive Gantt chart plot for a project schedule:

    >>> project_instance.plot_date_gantt(solution=schedule_df)

    This will display an interactive Gantt chart plot for the provided project schedule DataFrame. If the solution is not a valid DataFrame, it will attempt to generate one using the generate_datetime_schedule method.
    """

    def get_project_weekend_dates(SCHEDULE):

      project_date_range = pd.date_range(start= SCHEDULE['Start']['ES_date'], end = SCHEDULE['End']['EF_date'])
      weekend_dates = []
      for date in project_date_range:
        d_o_w = date.dayofweek
        if  d_o_w == 5 or d_o_w == 6:
          weekend_dates.append(date)
      return weekend_dates

    if not isinstance(solution,pd.core.frame.DataFrame):

      try:
        solution = self.generate_datetime_schedule(solution,start_date = None,date_format = '%Y-%m-%d',weekends_work = False,max_resources = None,verbose=False,save=False)
      except:
        raise ValueError('Sorry the solution provided is not a valid dataframe nor a valid schedule, please try generating the dataframe by calling the method generate_datetime_schedule')

    weekend_dates = get_project_weekend_dates(solution.T.to_dict())
    color_mapping = {True: 'red', False: 'blue'}

    if plot_type == 'plotly':

      fig_gantt_cpm = px.timeline(solution,
                                        x_start="ES_date",
                                        x_end="EF_date",
                                        y=solution.index,
                                        color = 'critical',
                                        color_discrete_map=color_mapping,
                                        hover_name = solution.index,
                                        hover_data= ['precedence','ES_date','ES_weekday','EF_weekday','EF_date','D','calendar_duration','critical'],
                                        category_orders={'index': solution.index[::-1]})
      for i in range(len(fig_gantt_cpm.data)):
                fig_gantt_cpm.data[i].marker.line.width = 2
                fig_gantt_cpm.data[i].marker.line.color = 'black'
      for date in weekend_dates:
          fig_gantt_cpm.add_shape(
              type="rect",
              x0= date,
              x1= date + datetime.timedelta(days=1),
              y0=-1,
              y1=len(solution),
              fillcolor="rgba(255, 0, 0, 0.1)",  # Adjust the color and opacity as needed
              layer="below",
              line_width=0,
          )
      fig_gantt_cpm.update_yaxes(autorange="reversed")
      fig_gantt_cpm.update_layout(xaxis_title="Date",yaxis_title="Activities")
      fig_gantt_cpm.show()

    if plot_type == 'matplotlib':

      fig, ax = plt.subplots(figsize=(10, 6))

      # Define colors
      color_mapping = {True: 'red', False: 'blue'}

      # Iterate through your data and plot bars
      for i, (es_date, ef_date, critical) in enumerate(zip(solution['ES_date'], solution['EF_date'], solution['critical'])):
          color = color_mapping[critical]
          ax.barh(i, (ef_date - es_date).days, left=es_date, color=color, edgecolor='black', linewidth=2)

      # Add weekend shading
      for date in weekend_dates:
          ax.axvspan(date, date + datetime.timedelta(days=1), color='red', alpha=0.1)

      # Set y-axis labels
      ax.set_yticks(range(len(solution)))
      ax.set_yticklabels(solution.index)

      # Set x-axis date formatting
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
      ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

      # Invert the y-axis to match Plotly's reversed layout
      ax.invert_yaxis()

      # Add labels
      plt.xlabel('Date')
      plt.ylabel('Activities')

      ax.tick_params(axis='x', rotation=90)

      # Show the plot
      plt.tight_layout()
      plt.show()


  def run_all_pl_heuristics(self,max_resources = None,plot_type = 'plotly'):

    """
    Run 24 priority rules from the RCPSP generative heuristics literature and generate schedules.

    This method applies 24 different priority rules to generate schedules for a project, including both Serial Schedule Generation (SSG)
    and Parallel Schedule Generation (PSG) methods.
    It stores the generated schedules and their makespan inside the instance and returns the best schedule found.
    It also generates an interactive Plotly bar chart to visualize the makespan of each schedule.

    Available priority rules include:

        - 'LPT': Longest processing time
        - 'SPT': Shortest processing time
        - 'LIS': Least immediate successors
        - 'MIS': Most immediate successor
        - 'LTS': Least total successors
        - 'MTS': Most total successors
        - 'sEST': Smallest Earliest Start Time
        - 'gEST': Greatest Earliest Start Time
        - 'sEFT': Smallest Earliest Finish Time
        - 'gEFT': Greatest Earliest Finish Time
        - 'sLST': Smallest Latest Start Time
        - 'gLST': Greatest Latest Start Time
        - 'sLFT': Smallest Latest Finish Time
        - 'gLFT': Greatest Latest Finish Time
        - 'MINF': Minimum float
        - 'MAXF': Maximum float
        - 'GRPW': Greatest GRPW
        - 'LRPW': Lowest GRPW
        - 'FCFS': First comes first served
        - 'LCFS': Last comes first served
        - 'GRD': Greatest resource demand
        - 'LRD': Lowest resource demand
        - 'GCRD': Greatest cumulative resource demand
        - 'LCRD': Lowest cumulative resource demand

    For reference, see:

    - "Heuristics for Scheduling Resource-Constrained Projects: An Experimental Investigation," Dale F. Cooper, 1976,
      Management Science, https://doi.org/10.1287/mnsc.22.11.1186
    - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 7)
    - Artigues, Christian, Sophie Demassey, and Emmanuel Neron, eds.
      Resource-constrained project scheduling: models, algorithms, extensions and applications. John Wiley & Sons, 2013. (Chapter 6)
    - Demeulemeester, Erik Leuven, and Willy S. Herroelen. Project scheduling: a research handbook. Vol. 49. Springer Science & Business Media, 2006. (Chapter 6)

    Parameters:
    ----------
    self : object
        The project instance to which this method belongs.
    max_resources : list, optional
        A list containing the limits of each resource used by the project. If not provided, it uses the maximum resources from the project instance.

    Returns:
    -------
    best : dictionary
        A dictionary containing information about the best schedule found, including the priority rule (PR), schedule method (SSG or PSG), the solution in the form of a dictionary, and the makespan of the schedule.

    Notes:
    -----
    This method runs 24 different priority rules and generates schedules for each one, comparing them to find the one with the lowest makespan.
    It stores the generated schedules inside the instance in the PL_list attribute and the best schedule in the best attribute.
    It also displays an interactive bar chart of makespans for each schedule.

    Examples:
    --------
    To run all 24 priority rules and generate schedules for a project:

    >>> project_instance.run_all_pl_heuristics(max_resources=max_resource_limits)

    This will apply all priority rules and return the best schedule found, along with generating an interactive bar chart to visualize the makespan of each schedule.
    """

    if max_resources is None:
      max_resources = self.max_resources

    priority_rules = {'LPT':['D',False], # Longest processing time
                      'SPT':['D',True], # shortest processing time
                      'LIS':['NUM_IS',True], # Least inmediate succesors
                      'MIS':['NUM_IS',False], # Most inmediate succesor
                      'LTS':['NUM_TS',True], # Least total succesors
                      'MTS':['NUM_TS',False], # Most total succesors
                      'sEST':['ES',True], # Smallest Earliest Start Time
                      'gEST':['ES',False], # Greatest Earliest Start Time
                      'sEFT':['EF',True], # Smallest Earliest Finish Time
                      'gEFT':['EF',False], # Greatest Earliest Finish Time
                      'sLST':['LS',True], # Smallest Latest Start Time
                      'gLST':['LS',False], # Greatest Latest Start Time
                      'sLFT':['LF',True], # Smallest Latest Finish Time
                      'gLFT':['LF',False], # Greatest Latest Finish Time
                      'MINF':['F',True], # Minimum float
                      'MAXF':['F',False], # Maximum float
                      'GRPW':['GRPW',False], # Greatest GRPW
                      'LRPW':['GRPW',True],# Greatest GRPW
                      'FCFS':['idx',True], # First comes first served
                      'LCFS':['idx',False], # Last comes first served
                      'GRD':['SUM_RES_IS',False], # Greatest resource demand
                      'LRD':['SUM_RES_IS',True], # lowest resource demand
                      'GCRD':['SUM_RES_TS',False], # Greatest cummulative resource demand
                      'LCRD':['SUM_RES_TS',True],} # lowest cummulative resource demand

    if not hasattr(self, 'PL_list'):
        self.PL_list = {}

    best = {'PR':None,'schedule_method':None,'solution':None,'makespan':sum(self.a_duration)}
    all_schedules = dict()
    for pr in tqdm(priority_rules):

      if pr in self.PL_list:
        pr_list = self.PL_list[pr]
      else:
        pr_list = self.get_priority_list(priority_rule= pr,verbose=False,save=True)

      ssg_schedule = self.SSG(pr_list,max_resources=max_resources,verbose=False,save=False)
      ssg_dur = ssg_schedule['End']['EF']

      if ssg_dur < best['makespan']:
        best = {'PR':pr,'schedule_method':'SSG','solution':ssg_schedule,'makespan':ssg_dur}

      psg_schedule = self.PSG(pr_list,max_resources=max_resources,verbose=False,save=False)
      psg_dur = psg_schedule['End']['EF']

      if psg_dur < best['makespan']:
        best = {'PR':pr,'schedule_method':'PSG','solution':psg_schedule,'makespan':psg_dur}
      all_schedules[pr] = {'SSG':ssg_schedule,'SSG_makespan':ssg_dur,'PSG':psg_schedule,'PSG_makespan':psg_dur}

    self.all_schedules = all_schedules
    self.best = best

    DF = pd.DataFrame(all_schedules).T
    DF = DF.drop(columns = ['SSG','PSG'])
    DF['SSG_makespan'] = DF['SSG_makespan'].astype(int)
    DF['PSG_makespan'] = DF['PSG_makespan'].astype(int)

    if plot_type == 'plotly':

      fig = px.bar(DF,x=DF.index,y = ['SSG_makespan','PSG_makespan'],
                  color_discrete_map={'SSG_makespan': 'blue', 'PSG_makespan': 'red'},barmode='group')
      fig.update_layout(xaxis_title='Priority rules',
                    yaxis_title='Project Makespan')
      fig.show()
    
    if plot_type == 'matplotlib':

      x_values = DF.index
      y_values_SSG = DF['SSG_makespan']
      y_values_PSG = DF['PSG_makespan']

      # Set bar width and positions
      bar_width = 0.35
      index = range(len(x_values))

      # Create the Matplotlib figure and axes
      fig, ax = plt.subplots(figsize=(16, 8))

      # Create bars for SSG_makespan
      plt.bar(index, y_values_SSG, bar_width, color='blue', label='SSG_makespan')

      # Create bars for PSG_makespan
      plt.bar([i + bar_width for i in index], y_values_PSG, bar_width, color='red', label='PSG_makespan')

      # Set x-axis labels
      plt.xticks([i + bar_width / 2 for i in index], x_values,rotation=45)

      # Set axis labels and plot title
      plt.xlabel('Priority rules')
      plt.ylabel('Project Makespan')
      plt.title('Bar Chart of Makespan by Priority Rules')

      # Add a legend
      plt.legend()

      # Show the plot
      plt.show()

    return best

  def monte_carlo_cpm_simple(self,pessimistic = 0.25, optimistic = 0.25, NumberIterations = 1_000):

    """
    Performs a Monte Carlo simulation for the project schedule using the Critical Path Method (CPM).
    This simulation introduces uncertainty by considering optimistic and pessimistic estimates
    for activity durations and generates multiple schedules to analyze schedule variability and key performance indicators.

    Output Indicators:

      * Activity Criticality Index (ACI):
      "In stochastic CPM, the critical path is not fixed. For instance, the occurrence of risks may
      alter the critical path in a given network. The Activity Criticality Index (ACI ) recognizes
      that almost any path and any activity can become critical with a certain probability (Van
      Slyke 1963). When using Monte Carlo simulation, the ACI of an activity is simply the
      proportion of simulation iterations during which the activity is critical." (extracted from CREEMERS et al 2014 doi:10.1007/s10479-013-1355)

      * Cruciality Index (CRI):
      "The Cruciality Index (CRI ) is defined as the absolute value of the correlation between the
      duration of an activity and the total project duration." (extracted from CREEMERS et al 2014 doi:10.1007/s10479-013-1355)

      * Schedule Sensitivity Index (SSI):
      "The PMI Body of Knowledge (2008) and Vanhoucke (2010) define a ranking index that combines ACI and the variance" (extracted from CREEMERS et al 2014 doi:10.1007/s10479-013-1355)

      * Spearman Rank Correlation (SRC):
      "Cho and Yum (1997) have criticized CRI because it assumes a linear relationship between
      the duration of an activity and the project completion time. They propose the use of a non-
      linear correlation measure such as the Spearman rank correlation coefficient." (extracted from CREEMERS et al 2014 doi:10.1007/s10479-013-1355)

    for reference see:

      - CREEMERS et al 2014 doi:10.1007/s10479-013-1355
      - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 5)

    Parameters
    ----------
    pessimistic : float, optional (default=0.25)
        The pessimistic estimate percentage (as a decimal) to be added to the center duration when defining the triangular distribution for activity durations.

    optimistic : float, optional (default=0.25)
        The optimistic estimate percentage (as a decimal) to be subtracted from the center duration when defining the triangular distribution for activity durations.

    NumberIterations : int, optional (default=1000)
        The number of Monte Carlo iterations to perform, each resulting in a different schedule based on the probabilistic activity durations.

    Returns
    -------
    output_df : DataFrame
        A summary statistics DataFrame containing key performance indicators (KPIs) for the Monte Carlo simulation. The DataFrame includes the following columns:
        - 'CPM_start': Planned Start date from the Critical Path Method
        - 'Mean_Duration': Mean duration of each activity.
        - 'Mean_Start': Mean start time of each activity.
        - 'Mean_Finish': Mean finish time of each activity.
        - '95%_Duration': 95th percentile duration of each activity.
        - '95%_Start': 95th percentile start time of each activity.
        - '95%_Finish': 95th percentile finish time of each activity.
        - '99%_Duration': 99th percentile duration of each activity.
        - '99%_Start': 99th percentile start time of each activity.
        - '99%_Finish': 99th percentile finish time of each activity.
        - 'Mean_Float': Mean float (slack) time of each activity.
        - 'ACI%': Activity Criticality Index (ACI) as a percentage of iterations during which the activity is critical.
        - 'CRI': Cruciality Index (CRI) representing the correlation between activity duration and project duration.
        - 'SRC': Spearman Rank Correlation (SRC) coefficient measuring non-linear correlation between activity duration and project duration.
        - 'SSI': Schedule Sensitivity Index (SSI) combining ACI and variance.
        - 'prob_on_time': Probability that the activity will start equal or below the CPM planned date

    Notes
    -----
    This method simulates project schedules by considering probabilistic activity durations based on optimistic and pessimistic estimates.
    It calculates various KPIs to assess schedule variability and criticality.

    Example
    -------
    To perform a Monte Carlo simulation with default parameters and obtain a summary statistics DataFrame, use the following:

    >>> output_df = project_instance.monte_carlo_cpm_simple()

    """

    def CPM(PROJECT): # Function that takes project input data and produces a CPM schedule

      CPM_SCHEDULE = dict()

      for task in PROJECT:
        CPM_SCHEDULE[task] = {'ES':0,'EF':0,'LS':0,'LF':0,'F':0,'D':PROJECT[task]['duration']}
        prec_constraints = PROJECT[task]['precedence']
        if prec_constraints == None or prec_constraints == 'None':
          continue
        #print(prec_constraints)
        starts = []
        for act in prec_constraints:
          starts.append(CPM_SCHEDULE[act]['EF']+PROJECT[act]['buffer'])
        CPM_SCHEDULE[task]['ES'] = max(starts)
        CPM_SCHEDULE[task]['EF'] = CPM_SCHEDULE[task]['ES'] + PROJECT[task]['duration']
        if task == 'End':
          CPM_SCHEDULE[task]['LS'] = CPM_SCHEDULE[task]['ES']
          CPM_SCHEDULE[task]['LF'] = CPM_SCHEDULE[task]['EF']


      for task in list(PROJECT.keys())[::-1]: # for each activity in the project but going from the end up to the start
        prec_constraints = PROJECT[task]['precedence'] # get the precedence constraints
        if prec_constraints == None or prec_constraints == 'None': # if the precedence constraint is none it means that the activity is the start
          continue
        for act in prec_constraints: # for each activity in the precedence constraint
          if CPM_SCHEDULE[act]['LF'] == 0:
            CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS'] - PROJECT[act]['buffer']# the late finish of the precedence c activitis equal to the start of the activity they precede
            CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration'] # the late start is equal to late finish minus the duration
          else:
            if CPM_SCHEDULE[task]['LS'] >= CPM_SCHEDULE[act]['LF']:
              continue
            else:
              CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS']- PROJECT[act]['buffer']
              CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration']
        CPM_SCHEDULE[task]['F'] = CPM_SCHEDULE[task]['LF'] - CPM_SCHEDULE[task]['EF'] # calculate the float

      return CPM_SCHEDULE



    if len(self.PROJECT) == 0:
      warnings.warn("!WARNING: Creating Project data dictionary...")
      self.create_project_dict()

    PROJECT = self.PROJECT
    n_activities = self.N

    for activity in PROJECT:

      PROJECT[activity]['optimistic'] = max(PROJECT[activity]['duration'] - PROJECT[activity]['duration']*optimistic,0)
      PROJECT[activity]['pesimistic'] = PROJECT[activity]['duration'] + PROJECT[activity]['duration']*pessimistic
      PROJECT[activity]['buffer'] = 0



    ActDurations = np.empty([n_activities, NumberIterations], dtype=float)

    for j,a in enumerate(PROJECT):
      for i in range(NumberIterations):
        if a == 'Start' or a=='End':
          ActDurations[j,i] = 0
        else:
          ActDurations[j,i] = np.random.triangular(PROJECT[a]['optimistic'],
                                                  PROJECT[a]['duration'],
                                                  PROJECT[a]['pesimistic'])

    ActStart = np.zeros([n_activities, NumberIterations], dtype=float)
    ActFinish = np.zeros([n_activities, NumberIterations], dtype=float)
    Floats = np.zeros([n_activities, NumberIterations], dtype=float)

    PROJECT_DF = pd.DataFrame(PROJECT).T

    for i in tqdm(range(NumberIterations),miniters=100,colour='green'):
      PROJECT_DF['duration'] = ActDurations[:,i]
      DATA = PROJECT_DF.T.to_dict()
      SCHEDULE = CPM(DATA)
      SCHEDULE_DF = pd.DataFrame(SCHEDULE)
      ActStart[:,i] = SCHEDULE_DF.T['ES'].values
      ActFinish[:,i] = SCHEDULE_DF.T['EF'].values
      Floats[:,i] = SCHEDULE_DF.T['F'].values

    cruciality = []
    src = []
    SSI = []
    y = ActFinish[n_activities-1,:]
    var_y = np.var(y)
    for i,a in enumerate(PROJECT):
      aci = np.count_nonzero(Floats[i,:].round()==0)/NumberIterations
      x = ActDurations[i,:]
      ssi = round(aci*np.sqrt(np.var(x)/var_y),2)
      SSI.append(ssi)
      coeff = round(np.corrcoef(x,y)[0,1],2)
      s_coeff = round(stats.spearmanr(x,y).correlation,2)
      src.append(s_coeff)
      cruciality.append(coeff)

    CPM_SCHEDULE = CPM(PROJECT)
    ES = [CPM_SCHEDULE[a]['ES'] for a in CPM_SCHEDULE]

    output_df = pd.DataFrame()
    output_df.index = list(PROJECT.keys())
    output_df['CPM_start'] = ES
    output_df['Mean_Duration'] = np.mean(ActDurations,axis=1).round(2)
    output_df['Mean_Start'] = np.mean(ActStart,axis=1).round(2)
    output_df['Mean_Finish'] = np.mean(ActFinish,axis=1).round(2)
    output_df['95%_Duration'] = np.quantile(ActDurations,0.95,axis=1).round(2)
    output_df['95%_Start'] = np.quantile(ActStart,0.95,axis=1).round(2)
    output_df['95%_Finish'] = np.quantile(ActFinish,0.95,axis=1).round(2)
    output_df['99%_Duration'] = np.quantile(ActDurations,0.99,axis=1).round(2)
    output_df['99%_Start'] = np.quantile(ActStart,0.99,axis=1).round(2)
    output_df['99%_Finish'] = np.quantile(ActFinish,0.99,axis=1).round(2)
    output_df['Mean_Float'] = np.mean(np.abs(Floats),axis=1).round(1)
    output_df['ACI%'] = np.count_nonzero(Floats.round()==0,axis=1)*100/NumberIterations
    output_df['CRI'] = cruciality
    output_df['SRC'] = src
    output_df['SSI'] = SSI

    probs = list()
    for i,a in enumerate(PROJECT):
      ES = CPM_SCHEDULE[a]['ES']
      prob = np.count_nonzero(ActStart[i,:] <= ES)*100/NumberIterations
      probs.append(prob)
    
    output_df['prob_on_time'] = probs

    return output_df

  def monte_carlo_cpm_detailed(self,pessimistic, optimistic, NumberIterations = 1_000):

    """
    Performs a Monte Carlo simulation for the project schedule using the Critical Path Method (CPM) on each iteration.

    The user provides a pessimistic value dictionary, a dictionary that contains the pessimistic durations for each activity.
    The user also provides an optimistic value dictionary, a dictionary that contains the optimistic durations for each activity,
    and the number of Monte Carlo iterations that the user wants to perform. For each iteration and for each activity in the project,
    the algorithm will create a triangular distribution with center = activity duration, lower = pessimistic duration, and upper = optimistic duration.
    With these new activity durations coming from the triangular distribution, the algorithm will generate a CPM schedule and it will store the results
    of the starting and ending date of each activity. The output of the method is a DataFrame with the summary statistics of the simulation.

    Output Indicators:

      * Activity Criticality Index (ACI):
      "In stochastic CPM, the critical path is not fixed. For instance, the occurrence of risks may
      alter the critical path in a given network. The Activity Criticality Index (ACI ) recognizes
      that almost any path and any activity can become critical with a certain probability (Van
      Slyke 1963). When using Monte Carlo simulation, the ACI of an activity is simply the
      proportion of simulation iterations during which the activity is critical." (extracted from CREEMERS et al 2014 doi:10.1007/s10479-013-1355)

      * Cruciality Index (CRI):
      "The Cruciality Index (CRI ) is defined as the absolute value of the correlation between the
      duration of an activity and the total project duration." (extracted from CREEMERS et al 2014 doi:10.1007/s10479-013-1355)

      * Schedule Sensitivity Index (SSI):
      "The PMI Body of Knowledge (2008) and Vanhoucke (2010) define a ranking index that combines ACI and the variance" (extracted from CREEMERS et al 2014 doi:10.1007/s10479-013-1355)

      * Spearman Rank Correlation (SRC):
      "Cho and Yum (1997) have criticized CRI because it assumes a linear relationship between
      the duration of an activity and the project completion time. They propose the use of a non-
      linear correlation measure such as the Spearman rank correlation coefficient." (extracted from CREEMERS et al 2014 doi:10.1007/s10479-013-1355)

    for reference see:

      - CREEMERS et al 2014 doi:10.1007/s10479-013-1355
      - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 5)

    Parameters:
    -----------
    pessimistic : dict
        A dictionary with each activity as a key and the value is the pessimistic duration.

    optimistic : dict
        A dictionary with each activity as a key and the value is the optimistic duration.

    NumberIterations : int, optional (default=1,000)
        Number of simulations for the Monte Carlo method.

    Returns:
    --------
    output_df : pandas DataFrame
        A DataFrame with a collection of metrics and summary statistics of the simulation, including:
        - 'CPM_start': Planned Start date from the Critical Path Method
        - 'Mean_Duration': Mean duration of each activity.
        - 'Mean_Start': Mean start time of each activity.
        - 'Mean_Finish': Mean finish time of each activity.
        - '95%_Duration': 95th percentile duration of each activity.
        - '95%_Start': 95th percentile start time of each activity.
        - '95%_Finish': 95th percentile finish time of each activity.
        - '99%_Duration': 99th percentile duration of each activity.
        - '99%_Start': 99th percentile start time of each activity.
        - '99%_Finish': 99th percentile finish time of each activity.
        - 'Mean_Float': Mean float (slack) time of each activity.
        - 'ACI%': Activity Criticality Index (ACI) as a percentage of iterations during which the activity is critical.
        - 'CRI': Cruciality Index (CRI) representing the correlation between activity duration and project duration.
        - 'SRC': Spearman Rank Correlation (SRC) coefficient measuring non-linear correlation between activity duration and project duration.
        - 'SSI': Schedule Sensitivity Index (SSI) combining ACI and variance.
        - 'prob_on_time': Probability that the activity will start equal or below the CPM planned date

    Notes:
    ------
    - The function relies on the CPM function within the code to generate CPM schedules for each iteration.

    Example:
    --------
    >>> pessimistic = {'TaskA': 10, 'TaskB': 15, 'TaskC': 8}
    >>> optimistic = {'TaskA': 5, 'TaskB': 12, 'TaskC': 6}
    >>> iterations = 1000
    >>> result_df = monte_carlo_cpm_detailed(pessimistic, optimistic, iterations)
    >>> print(result_df)

    See Also:
    ---------
    - method: self.CPM().
    """

    def CPM(PROJECT): # Function that takes project input data and produces a CPM schedule

      CPM_SCHEDULE = dict()

      for task in PROJECT:
        CPM_SCHEDULE[task] = {'ES':0,'EF':0,'LS':0,'LF':0,'F':0,'D':PROJECT[task]['duration']}
        prec_constraints = PROJECT[task]['precedence']
        if prec_constraints == None or prec_constraints == 'None':
          continue
        #print(prec_constraints)
        starts = []
        for act in prec_constraints:
          starts.append(CPM_SCHEDULE[act]['EF']+PROJECT[act]['buffer'])
        CPM_SCHEDULE[task]['ES'] = max(starts)
        CPM_SCHEDULE[task]['EF'] = CPM_SCHEDULE[task]['ES'] + PROJECT[task]['duration']
        if task == 'End':
          CPM_SCHEDULE[task]['LS'] = CPM_SCHEDULE[task]['ES']
          CPM_SCHEDULE[task]['LF'] = CPM_SCHEDULE[task]['EF']


      for task in list(PROJECT.keys())[::-1]: # for each activity in the project but going from the end up to the start
        prec_constraints = PROJECT[task]['precedence'] # get the precedence constraints
        if prec_constraints == None or prec_constraints == 'None': # if the precedence constraint is none it means that the activity is the start
          continue
        for act in prec_constraints: # for each activity in the precedence constraint
          if CPM_SCHEDULE[act]['LF'] == 0:
            CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS'] - PROJECT[act]['buffer']# the late finish of the precedence c activitis equal to the start of the activity they precede
            CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration'] # the late start is equal to late finish minus the duration
          else:
            if CPM_SCHEDULE[task]['LS'] >= CPM_SCHEDULE[act]['LF']:
              continue
            else:
              CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS']- PROJECT[act]['buffer']
              CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration']
        CPM_SCHEDULE[task]['F'] = CPM_SCHEDULE[task]['LF'] - CPM_SCHEDULE[task]['EF'] # calculate the float

      return CPM_SCHEDULE

    if len(self.PROJECT) == 0:
      warnings.warn("!WARNING: Creating Project data dictionary...")
      self.create_project_dict()

    PROJECT = self.PROJECT
    n_activities = self.N

    for activity in PROJECT:

      PROJECT[activity]['optimistic'] = optimistic.get(activity,PROJECT[activity]['duration'])
      PROJECT[activity]['pesimistic'] = pessimistic.get(activity,PROJECT[activity]['duration'])
      PROJECT[activity]['buffer'] = 0

    ActDurations = np.empty([n_activities, NumberIterations], dtype=float)

    for j,a in enumerate(PROJECT):
      for i in range(NumberIterations):
        if a == 'Start' or a=='End':
          ActDurations[j,i] = 0
        else:
          ActDurations[j,i] = np.random.triangular(PROJECT[a]['optimistic'],
                                                  PROJECT[a]['duration'],
                                                  PROJECT[a]['pesimistic'])

    ActStart = np.zeros([n_activities, NumberIterations], dtype=float)
    ActFinish = np.zeros([n_activities, NumberIterations], dtype=float)
    Floats = np.zeros([n_activities, NumberIterations], dtype=float)

    PROJECT_DF = pd.DataFrame(PROJECT).T

    for i in tqdm(range(NumberIterations),miniters=100,colour='green'):
      PROJECT_DF['duration'] = ActDurations[:,i]
      DATA = PROJECT_DF.T.to_dict()
      SCHEDULE = CPM(DATA)
      SCHEDULE_DF = pd.DataFrame(SCHEDULE)
      ActStart[:,i] = SCHEDULE_DF.T['ES'].values
      ActFinish[:,i] = SCHEDULE_DF.T['EF'].values
      Floats[:,i] = SCHEDULE_DF.T['F'].values

    cruciality = []
    src = []
    SSI = []
    y = ActFinish[n_activities-1,:]
    var_y = np.var(y)
    for i,a in enumerate(PROJECT):
      aci = np.count_nonzero(Floats[i,:].round()==0)/NumberIterations
      x = ActDurations[i,:]
      ssi = round(aci*np.sqrt(np.var(x)/var_y),2)
      SSI.append(ssi)
      coeff = round(np.corrcoef(x,y)[0,1],2)
      s_coeff = round(stats.spearmanr(x,y).correlation,2)
      src.append(s_coeff)
      cruciality.append(coeff)

    CPM_SCHEDULE = CPM(PROJECT)
    ES = [CPM_SCHEDULE[a]['ES'] for a in CPM_SCHEDULE]

    output_df = pd.DataFrame()
    output_df.index = list(PROJECT.keys())
    output_df['CPM_start'] = ES
    output_df['Mean_Duration'] = np.mean(ActDurations,axis=1).round(2)
    output_df['Mean_Start'] = np.mean(ActStart,axis=1).round(2)
    output_df['Mean_Finish'] = np.mean(ActFinish,axis=1).round(2)
    output_df['95%_Duration'] = np.quantile(ActDurations,0.95,axis=1).round(2)
    output_df['95%_Start'] = np.quantile(ActStart,0.95,axis=1).round(2)
    output_df['95%_Finish'] = np.quantile(ActFinish,0.95,axis=1).round(2)
    output_df['99%_Duration'] = np.quantile(ActDurations,0.99,axis=1).round(2)
    output_df['99%_Start'] = np.quantile(ActStart,0.99,axis=1).round(2)
    output_df['99%_Finish'] = np.quantile(ActFinish,0.99,axis=1).round(2)
    output_df['Mean_Float'] = np.mean(np.abs(Floats),axis=1).round(1)
    output_df['ACI%'] = np.count_nonzero(Floats.round()==0,axis=1)*100/NumberIterations
    output_df['CRI'] = cruciality
    output_df['SRC'] = src
    output_df['SSI'] = SSI

    probs = list()
    for i,a in enumerate(PROJECT):
      ES = CPM_SCHEDULE[a]['ES']
      prob = np.count_nonzero(ActStart[i,:] <= ES)*100/NumberIterations
      probs.append(prob)
    
    output_df['prob_on_time'] = probs

    return output_df

  def monte_carlo_simple_buffer_analysis(self,pessimistic = 0.25, optimistic = 0.25, buffer = None, NumberIterations = 1_000):


    """
    Performs a Monte Carlo simulation for project schedule analysis with buffer consideration.

    This method conducts Monte Carlo simulations using the Critical Path Method (CPM) for project scheduling.
    The user provides a pessimistic value dictionary, which contains pessimistic durations for each activity, an optimistic value dictionary
    with optimistic durations for each activity, a buffer dictionary specifying buffer sizes for each activity, and the number of Monte Carlo
    iterations to perform. For each iteration and each activity in the project, the algorithm creates a triangular distribution with:
    - Center = Activity duration
    - Lower = Pessimistic duration
    - Upper = Optimistic duration

    The algorithm generates a CPM schedule based on these new activity durations and stores the results of the starting and ending dates
    of each activity. It also inserts a time buffer of the size specified by the user after each activity and determines whether the buffer
    size was sufficient to account for the uncertainty in the activity's duration. The final output is the probability that an activity will
    start on its planned start date, given the buffer specified by the user.

    for reference see:

      - CREEMERS et al 2014 doi:10.1007/s10479-013-1355
      - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 5)

    Parameters:
    -----------
    pessimistic : float, optional (default=0.25)
        The pessimistic estimate percentage (as a decimal) to be added to the center duration when defining the triangular distribution for activity durations.

    optimistic : float, optional (default=0.25)
        The optimistic estimate percentage (as a decimal) to be subtracted from the center duration when defining the triangular distribution for activity durations.
    buffer : dict
        A dictionary with each activity as a key and the buffer size as the values.

    NumberIterations : int, optional (default=1,000)
        Number of simulations for the Monte Carlo method.

    Returns:
    --------
    buffer_df : pandas DataFrame
        A DataFrame with the final statistics and summary Key Performance Indicators (KPIs) from the Monte Carlo simulation, including:
        - buffer: Buffer size for each activity.
        - mean_duration: Mean duration of each activity.
        - planned_start: Planned start time for each activity.
        - mean_start: Mean start time of each activity after considering buffers.
        - 95%_start: 95th percentile start time of each activity after considering buffers.
        - 99%_start: 99th percentile start time of each activity after considering buffers.
        - prob_on_time: Probability that an activity will start on time, given the specified buffer.

    Notes:
    ------
    - The function relies on the CPM and CPM_MC functions within the code to generate CPM schedules for each iteration with buffer analysis.

    Example:
    --------
    >>> pessimistic = 0.25
    >>> optimistic = 0.25
    >>> buffer = {'TaskA': 2, 'TaskB': 1, 'TaskC': 0}
    >>> iterations = 1000
    >>> result_df = monte_carlo_detail_buffer_analysis(pessimistic, optimistic, buffer, iterations)
    >>> print(result_df)
    """

    def CPM(PROJECT): # Function that takes project input data and produces a CPM schedule

      CPM_SCHEDULE = dict()

      for task in PROJECT:
        CPM_SCHEDULE[task] = {'ES':0,'EF':0,'LS':0,'LF':0,'F':0,'D':PROJECT[task]['duration']}
        prec_constraints = PROJECT[task]['precedence']
        if prec_constraints == None or prec_constraints == 'None':
          continue
        #print(prec_constraints)
        starts = []
        for act in prec_constraints:
          starts.append(CPM_SCHEDULE[act]['EF']+PROJECT[act]['buffer'])
        CPM_SCHEDULE[task]['ES'] = max(starts)
        CPM_SCHEDULE[task]['EF'] = CPM_SCHEDULE[task]['ES'] + PROJECT[task]['duration']
        if task == 'End':
          CPM_SCHEDULE[task]['LS'] = CPM_SCHEDULE[task]['ES']
          CPM_SCHEDULE[task]['LF'] = CPM_SCHEDULE[task]['EF']


      for task in list(PROJECT.keys())[::-1]: # for each activity in the project but going from the end up to the start
        prec_constraints = PROJECT[task]['precedence'] # get the precedence constraints
        if prec_constraints == None or prec_constraints == 'None': # if the precedence constraint is none it means that the activity is the start
          continue
        for act in prec_constraints: # for each activity in the precedence constraint
          if CPM_SCHEDULE[act]['LF'] == 0:
            CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS'] - PROJECT[act]['buffer']# the late finish of the precedence c activitis equal to the start of the activity they precede
            CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration'] # the late start is equal to late finish minus the duration
          else:
            if CPM_SCHEDULE[task]['LS'] >= CPM_SCHEDULE[act]['LF']:
              continue
            else:
              CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS']- PROJECT[act]['buffer']
              CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration']
        CPM_SCHEDULE[task]['F'] = CPM_SCHEDULE[task]['LF'] - CPM_SCHEDULE[task]['EF'] # calculate the float

      return CPM_SCHEDULE

    def CPM_MC(PROJECT,MC_DURATIONS): # Function that takes project input data and produces a CPM schedule

      CPM_SCHEDULE = dict()

      for task in PROJECT:
        a_duration = round(max(PROJECT[task]['duration'] + PROJECT[task]['buffer'],MC_DURATIONS[task]),1)
        CPM_SCHEDULE[task] = {'ES':0,'EF':0,'LS':0,'LF':0,'F':0,'D':a_duration,'iD':PROJECT[task]['duration']}
        prec_constraints = PROJECT[task]['precedence']
        if prec_constraints == None or prec_constraints == 'None':
          continue
        #print(prec_constraints)
        starts = []
        for act in prec_constraints:
          starts.append(CPM_SCHEDULE[act]['EF'])
        CPM_SCHEDULE[task]['ES'] = max(starts)

        CPM_SCHEDULE[task]['EF'] = CPM_SCHEDULE[task]['ES'] + a_duration
        if task == 'End':
          CPM_SCHEDULE[task]['LS'] = CPM_SCHEDULE[task]['ES']
          CPM_SCHEDULE[task]['LF'] = CPM_SCHEDULE[task]['EF']


      for task in list(PROJECT.keys())[::-1]: # for each activity in the project but going from the end up to the start

        prec_constraints = PROJECT[task]['precedence'] # get the precedence constraints
        if prec_constraints == None or prec_constraints == 'None': # if the precedence constraint is none it means that the activity is the start
          continue
        for act in prec_constraints: # for each activity in the precedence constraint
          if CPM_SCHEDULE[act]['LF'] == 0:
            CPM_SCHEDULE[act]['LF'] = round(CPM_SCHEDULE[task]['LS'],1) # the late finish of the precedence c activitis equal to the start of the activity they precede
            CPM_SCHEDULE[act]['LS'] = round(CPM_SCHEDULE[act]['LF'] - CPM_SCHEDULE[act]['D'],1)  # the late start is equal to late finish minus the duration
          else:
            if CPM_SCHEDULE[task]['LS'] >= CPM_SCHEDULE[act]['LF']:
              continue
            else:
              CPM_SCHEDULE[act]['LF'] = round(CPM_SCHEDULE[task]['LS'],1)
              CPM_SCHEDULE[act]['LS'] = round(CPM_SCHEDULE[act]['LF'] - CPM_SCHEDULE[act]['D'],1)
        CPM_SCHEDULE[task]['F'] = CPM_SCHEDULE[task]['LF'] - CPM_SCHEDULE[task]['EF'] # calculate the float

      return CPM_SCHEDULE

    if len(self.PROJECT) == 0:
      warnings.warn("!WARNING: Creating Project data dictionary...")
      self.create_project_dict()
    
    if buffer == None:
      raise ValueError('Buffer cannot be empty. Buffer must be a dictionary with the amount of days that should be inserted after the end date of an activity')

    PROJECT = self.PROJECT
    n_activities = self.N

    for activity in PROJECT:
      
      PROJECT[activity]['optimistic'] = max(PROJECT[activity]['duration'] - PROJECT[activity]['duration']*optimistic,0)
      PROJECT[activity]['pesimistic'] = PROJECT[activity]['duration'] + PROJECT[activity]['duration']*pessimistic
      PROJECT[activity]['buffer'] = buffer.get(activity,0)

    PROJECT_DF = pd.DataFrame(PROJECT).T
    CPM_SCHEDULE = CPM(PROJECT)

    ActDurations = np.empty([n_activities, NumberIterations], dtype=float)

    for j,a in enumerate(PROJECT):
      for i in range(NumberIterations):
        if a == 'Start' or a=='End':
          ActDurations[j,i] = 0
        else:
          ActDurations[j,i] = np.random.triangular(PROJECT[a]['optimistic'],
                                                  PROJECT[a]['duration'],
                                                  PROJECT[a]['pesimistic'])

    ActStart = np.zeros([n_activities, NumberIterations], dtype=float)
    ActFinish = np.zeros([n_activities, NumberIterations], dtype=float)
    Floats = np.zeros([n_activities, NumberIterations], dtype=float)

    ActStart_BF = np.zeros([n_activities, NumberIterations], dtype=float)

    for i in tqdm(range(NumberIterations),miniters=100,colour='green'):
      PROJECT_DF['duration'] = ActDurations[:,i]
      MC_DURATIONS = PROJECT_DF['duration'].to_dict()
      SCHEDULE = CPM_MC(PROJECT,MC_DURATIONS)
      SCHEDULE_DF = pd.DataFrame(SCHEDULE)
      ActStart_BF[:,i] = SCHEDULE_DF.T['ES'].values

    probs_start_on_time = []
    ideal_start = []
    for i,a in enumerate(PROJECT):
      st = CPM_SCHEDULE[a]['ES']
      ideal_start.append(st)
      x = ActStart_BF[i,:]
      b = np.count_nonzero(x <= st)/NumberIterations
      probs_start_on_time.append(round((b)*100,2))

    buffer_df = pd.DataFrame()
    buffer_df.index = list(PROJECT.keys())

    PROJECT = self.PROJECT
    for a in PROJECT:
      PROJECT[a]['buffer'] = 0
    CPM_SCHEDULE = CPM(PROJECT)
    ES = [CPM_SCHEDULE[a]['ES'] for a in CPM_SCHEDULE]

    buffer_df['buffer']=PROJECT_DF['buffer'].values
    buffer_df['CPM_start_wo_buff'] = ES
    buffer_df['mean_duration'] = np.mean(ActDurations,axis=1).round(2)
    buffer_df['planned_start'] = ideal_start
    buffer_df['mean_start'] = np.mean(ActStart_BF,axis=1).round(2)
    buffer_df['95%_start'] = np.quantile(ActStart_BF,0.95,axis=1).round(2)
    buffer_df['99%_start'] = np.quantile(ActStart_BF,0.99,axis=1).round(2)
    buffer_df['prob_on_time'] = probs_start_on_time

    return buffer_df

  def monte_carlo_detail_buffer_analysis(self,pessimistic, optimistic, buffer, NumberIterations = 1_000):


    """
    Performs a Monte Carlo simulation for project schedule analysis with buffer consideration.

    This method conducts Monte Carlo simulations using the Critical Path Method (CPM) for project scheduling.
    The user provides a pessimistic value dictionary, which contains pessimistic durations for each activity, an optimistic value dictionary
    with optimistic durations for each activity, a buffer dictionary specifying buffer sizes for each activity, and the number of Monte Carlo
    iterations to perform. For each iteration and each activity in the project, the algorithm creates a triangular distribution with:
    - Center = Activity duration
    - Lower = Pessimistic duration
    - Upper = Optimistic duration

    The algorithm generates a CPM schedule based on these new activity durations and stores the results of the starting and ending dates
    of each activity. It also inserts a time buffer of the size specified by the user after each activity and determines whether the buffer
    size was sufficient to account for the uncertainty in the activity's duration. The final output is the probability that an activity will
    start on its planned start date, given the buffer specified by the user.

    for reference see:

      - CREEMERS et al 2014 doi:10.1007/s10479-013-1355
      - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 5)

    Parameters:
    -----------
    pessimistic : dict
        A dictionary with each activity as a key and the value is the pessimistic duration.

    optimistic : dict
        A dictionary with each activity as a key and the value is the optimistic duration.

    buffer : dict
        A dictionary with each activity as a key and the buffer size as the values.

    NumberIterations : int, optional (default=1,000)
        Number of simulations for the Monte Carlo method.

    Returns:
    --------
    buffer_df : pandas DataFrame
        A DataFrame with the final statistics and summary Key Performance Indicators (KPIs) from the Monte Carlo simulation, including:
        - buffer: Buffer size for each activity.
        - mean_duration: Mean duration of each activity.
        - planned_start: Planned start time for each activity.
        - mean_start: Mean start time of each activity after considering buffers.
        - 95%_start: 95th percentile start time of each activity after considering buffers.
        - 99%_start: 99th percentile start time of each activity after considering buffers.
        - prob_on_time: Probability that an activity will start on time, given the specified buffer.

    Notes:
    ------
    - The function relies on the CPM and CPM_MC functions within the code to generate CPM schedules for each iteration with buffer analysis.

    Example:
    --------
    >>> pessimistic = {'TaskA': 10, 'TaskB': 15, 'TaskC': 8}
    >>> optimistic = {'TaskA': 5, 'TaskB': 12, 'TaskC': 6}
    >>> buffer = {'TaskA': 2, 'TaskB': 1, 'TaskC': 0}
    >>> iterations = 1000
    >>> result_df = monte_carlo_detail_buffer_analysis(pessimistic, optimistic, buffer, iterations)
    >>> print(result_df)
    """

    def CPM(PROJECT): # Function that takes project input data and produces a CPM schedule

      CPM_SCHEDULE = dict()

      for task in PROJECT:
        CPM_SCHEDULE[task] = {'ES':0,'EF':0,'LS':0,'LF':0,'F':0,'D':PROJECT[task]['duration']}
        prec_constraints = PROJECT[task]['precedence']
        if prec_constraints == None or prec_constraints == 'None':
          continue
        #print(prec_constraints)
        starts = []
        for act in prec_constraints:
          starts.append(CPM_SCHEDULE[act]['EF']+PROJECT[act]['buffer'])
        CPM_SCHEDULE[task]['ES'] = max(starts)
        CPM_SCHEDULE[task]['EF'] = CPM_SCHEDULE[task]['ES'] + PROJECT[task]['duration']
        if task == 'End':
          CPM_SCHEDULE[task]['LS'] = CPM_SCHEDULE[task]['ES']
          CPM_SCHEDULE[task]['LF'] = CPM_SCHEDULE[task]['EF']


      for task in list(PROJECT.keys())[::-1]: # for each activity in the project but going from the end up to the start
        prec_constraints = PROJECT[task]['precedence'] # get the precedence constraints
        if prec_constraints == None or prec_constraints == 'None': # if the precedence constraint is none it means that the activity is the start
          continue
        for act in prec_constraints: # for each activity in the precedence constraint
          if CPM_SCHEDULE[act]['LF'] == 0:
            CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS'] - PROJECT[act]['buffer']# the late finish of the precedence c activitis equal to the start of the activity they precede
            CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration'] # the late start is equal to late finish minus the duration
          else:
            if CPM_SCHEDULE[task]['LS'] >= CPM_SCHEDULE[act]['LF']:
              continue
            else:
              CPM_SCHEDULE[act]['LF'] = CPM_SCHEDULE[task]['LS']- PROJECT[act]['buffer']
              CPM_SCHEDULE[act]['LS'] = CPM_SCHEDULE[act]['LF'] - PROJECT[act]['duration']
        CPM_SCHEDULE[task]['F'] = CPM_SCHEDULE[task]['LF'] - CPM_SCHEDULE[task]['EF'] # calculate the float

      return CPM_SCHEDULE

    def CPM_MC(PROJECT,MC_DURATIONS): # Function that takes project input data and produces a CPM schedule

      CPM_SCHEDULE = dict()

      for task in PROJECT:
        a_duration = round(max(PROJECT[task]['duration'] + PROJECT[task]['buffer'],MC_DURATIONS[task]),1)
        CPM_SCHEDULE[task] = {'ES':0,'EF':0,'LS':0,'LF':0,'F':0,'D':a_duration,'iD':PROJECT[task]['duration']}
        prec_constraints = PROJECT[task]['precedence']
        if prec_constraints == None or prec_constraints == 'None':
          continue
        #print(prec_constraints)
        starts = []
        for act in prec_constraints:
          starts.append(CPM_SCHEDULE[act]['EF'])
        CPM_SCHEDULE[task]['ES'] = max(starts)

        CPM_SCHEDULE[task]['EF'] = CPM_SCHEDULE[task]['ES'] + a_duration
        if task == 'End':
          CPM_SCHEDULE[task]['LS'] = CPM_SCHEDULE[task]['ES']
          CPM_SCHEDULE[task]['LF'] = CPM_SCHEDULE[task]['EF']


      for task in list(PROJECT.keys())[::-1]: # for each activity in the project but going from the end up to the start

        prec_constraints = PROJECT[task]['precedence'] # get the precedence constraints
        if prec_constraints == None or prec_constraints == 'None': # if the precedence constraint is none it means that the activity is the start
          continue
        for act in prec_constraints: # for each activity in the precedence constraint
          if CPM_SCHEDULE[act]['LF'] == 0:
            CPM_SCHEDULE[act]['LF'] = round(CPM_SCHEDULE[task]['LS'],1) # the late finish of the precedence c activitis equal to the start of the activity they precede
            CPM_SCHEDULE[act]['LS'] = round(CPM_SCHEDULE[act]['LF'] - CPM_SCHEDULE[act]['D'],1)  # the late start is equal to late finish minus the duration
          else:
            if CPM_SCHEDULE[task]['LS'] >= CPM_SCHEDULE[act]['LF']:
              continue
            else:
              CPM_SCHEDULE[act]['LF'] = round(CPM_SCHEDULE[task]['LS'],1)
              CPM_SCHEDULE[act]['LS'] = round(CPM_SCHEDULE[act]['LF'] - CPM_SCHEDULE[act]['D'],1)
        CPM_SCHEDULE[task]['F'] = CPM_SCHEDULE[task]['LF'] - CPM_SCHEDULE[task]['EF'] # calculate the float

      return CPM_SCHEDULE

    if len(self.PROJECT) == 0:
      warnings.warn("!WARNING: Creating Project data dictionary...")
      self.create_project_dict()

    PROJECT = self.PROJECT
    n_activities = self.N

    for activity in PROJECT:

      PROJECT[activity]['optimistic'] = optimistic.get(activity,PROJECT[activity]['duration'])
      PROJECT[activity]['pesimistic'] = pessimistic.get(activity,PROJECT[activity]['duration'])
      PROJECT[activity]['buffer'] = buffer.get(activity,0)

    PROJECT_DF = pd.DataFrame(PROJECT).T
    CPM_SCHEDULE = CPM(PROJECT)

    ActDurations = np.empty([n_activities, NumberIterations], dtype=float)

    for j,a in enumerate(PROJECT):
      for i in range(NumberIterations):
        if a == 'Start' or a=='End':
          ActDurations[j,i] = 0
        else:
          ActDurations[j,i] = np.random.triangular(PROJECT[a]['optimistic'],
                                                  PROJECT[a]['duration'],
                                                  PROJECT[a]['pesimistic'])

    ActStart = np.zeros([n_activities, NumberIterations], dtype=float)
    ActFinish = np.zeros([n_activities, NumberIterations], dtype=float)
    Floats = np.zeros([n_activities, NumberIterations], dtype=float)

    ActStart_BF = np.zeros([n_activities, NumberIterations], dtype=float)

    for i in tqdm(range(NumberIterations),miniters=100,colour='green'):
      PROJECT_DF['duration'] = ActDurations[:,i]
      MC_DURATIONS = PROJECT_DF['duration'].to_dict()
      SCHEDULE = CPM_MC(PROJECT,MC_DURATIONS)
      SCHEDULE_DF = pd.DataFrame(SCHEDULE)
      ActStart_BF[:,i] = SCHEDULE_DF.T['ES'].values

    probs_start_on_time = []
    ideal_start = []
    for i,a in enumerate(PROJECT):
      st = CPM_SCHEDULE[a]['ES']
      ideal_start.append(st)
      x = ActStart_BF[i,:]
      b = np.count_nonzero(x <= st)/NumberIterations
      probs_start_on_time.append(round((b)*100,2))

    buffer_df = pd.DataFrame()
    buffer_df.index = list(PROJECT.keys())

    PROJECT = self.PROJECT
    for a in PROJECT:
      PROJECT[a]['buffer'] = 0
    CPM_SCHEDULE = CPM(PROJECT)
    ES = [CPM_SCHEDULE[a]['ES'] for a in CPM_SCHEDULE]

    buffer_df['buffer']=PROJECT_DF['buffer'].values
    buffer_df['CPM_start_wo_buff'] = ES
    buffer_df['mean_duration'] = np.mean(ActDurations,axis=1).round(2)
    buffer_df['planned_start'] = ideal_start
    buffer_df['mean_start'] = np.mean(ActStart_BF,axis=1).round(2)
    buffer_df['95%_start'] = np.quantile(ActStart_BF,0.95,axis=1).round(2)
    buffer_df['99%_start'] = np.quantile(ActStart_BF,0.99,axis=1).round(2)
    buffer_df['prob_on_time'] = probs_start_on_time

    return buffer_df

  def genetic_algorithm_optimization(self,max_resources = None, popSize = 40,elite_percentage = 0.2,
                                     crossover_rate = 0.2, mutationRate = 0.05, generations = 100,show=False,initial_solution=None):

    """
    Implements a genetic algorithm to solve the RCPSP (Resource-Constrained Project Scheduling Problem).

    This method utilizes a genetic algorithm to find an optimal solution for the Resource-Constrained Project Scheduling Problem (RCPSP).
    Internally, it employs constructive priority list generation methods,
    as well as the SSG (Serial Schedule Generation) and PSG (Parallel Schedule Generation) scheduling algorithms.
    The algorithm returns the best solution found after a specified number of generations.

    For references see:
      - Taillard, Éric D. Design of heuristic algorithms for hard optimization: with python codes for the travelling salesman problem. Springer Nature, 2023.
      - Ferrante Neri, Carlos Cotta, and Pablo Moscato. "Handbook of memetic algorithms." Studies in Computational Intelligence. Springer (2011)
      - "Heuristics for Scheduling Resource-Constrained Projects: An Experimental Investigation," Dale F. Cooper, 1976,
        Management Science, https://doi.org/10.1287/mnsc.22.11.1186
      - Vanhoucke, Mario. Project management with dynamic scheduling. Springer Berlin Heidelberg, 2012. (Chapter 7)
      - Artigues, Christian, Sophie Demassey, and Emmanuel Neron, eds.
      Resource-constrained project scheduling: models, algorithms, extensions and applications. John Wiley & Sons, 2013. (Chapter 6)
      - Demeulemeester, Erik Leuven, and Willy S. Herroelen. Project scheduling: a research handbook. Vol. 49. Springer Science & Business Media, 2006. (Chapter 6)


    Parameters:
    -----------
    max_resources : list, optional (default=None)
        List of the limits of resources for each resource consumed by the project.

    popSize : int, optional (default=40)
        Population size for the genetic algorithm.

    elite_percentage : float, optional (default=0.2)
        Metaparameter representing the percentage of the population that is retained for the next generation.

    crossover_rate : float, optional (default=0.2)
        Metaparameter describing the probability that two chromosomes (solutions) will mate during crossover.

    mutationRate : float, optional (default=0.05)
        Metaparameter describing the probability of a gene mutation in a chromosome.

    generations : int, optional (default=100)
        Number of generations for the genetic algorithm.

    show : bool, optional (default=False)
        If True, the progress of the algorithm and the best chromosome of each generation are displayed.
        Additionally, a matplotlib line graph with a summary of the optimization method's behavior throughout the process is shown.

    Returns:
    --------
    best : chromosome
        The best chromosome found by the genetic algorithm.
        This chromosome is also stored as an attribute inside the instance (self.best).

    Notes:
    ------
    - The genetic algorithm is designed to find an optimal schedule for the Resource-Constrained Project Scheduling Problem (RCPSP).

    Example:
    --------
    >>> max_resources = [10, 15, 20]
    >>> popSize = 50
    >>> elite_percentage = 0.2
    >>> crossover_rate = 0.3
    >>> mutationRate = 0.1
    >>> generations = 200
    >>> show = True
    >>> result_chromosome = genetic_algorithm_optimization(max_resources, popSize, elite_percentage, crossover_rate, mutationRate, generations, show)
    >>> print(result_chromosome)

    See Also:
    ---------
    - Constructive priority list generation methods, SSG, PSG scheduling algorithms for RCPSP.
    - Matplotlib for visualizing optimization progress (if show=True).
    """

    def create_chromosome(PROJECT):
      c = [x for x in PROJECT] + [1]
      new_schedule = list(np.random.choice(c[1:-2],len(c)-3,replace=False))
      p3 = np.random.choice([1,2],1)[0]
      new_schedule = ['Start'] + new_schedule + ['End'] + [p3]
      return new_schedule

    def initialPopulation(popSize, PROJECT,initial_solution=None):
      c = [x for x in PROJECT] + [1]
      d = [x for x in PROJECT] + [2]
      

      if initial_solution is None:
        population = [c,d]
        for i in range(0, popSize-2):
            population.append(create_chromosome(PROJECT))
      
      if initial_solution is not None:
        
        #print('Initial solution used :D')
        e = initial_solution + [1]
        f = initial_solution + [2]

        population = [c,d,f,e]
        for i in range(0, popSize-4):
            population.append(create_chromosome(PROJECT))
      return population

    def is_PL_valid(PL):

      valid = 0
      for n1,n2 in EDGES:

        if PL.index(n1) < PL.index(n2):
          valid +=1

      if valid == len(EDGES):
        return True
      else:
        return False

    def Fitness(solution):

      schedule_method = solution[-1]
      PL = solution[:-1]

      if is_PL_valid(PL):
        if schedule_method == 1:
          return ph/self.SSG(PL,max_resources=max_resources,verbose=False,save=False)['End']['EF']
        else:
          return ph/self.PSG(PL,max_resources=max_resources,verbose=False,save=False)['End']['EF']
      else:
        return 1

    def rankSchedules(population):
      fitnessResults = {}
      for i in range(0,len(population)):
          fitnessResults[i] = Fitness(population[i])
      return sorted(fitnessResults.items(),key=lambda item: item[1], reverse = True)

    def selection(popRanked, elite_percentage):

      eliteSize = int(len(popRanked)*elite_percentage)

      selectionResults = []
      df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
      df['cum_sum'] = df.Fitness.cumsum()
      df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()

      for i in range(0, eliteSize):
          selectionResults.append(popRanked[i][0])
      for i in range(0, len(popRanked) - eliteSize):
          pick = 100*np.random.rand()
          for i in range(0, len(popRanked)):
              if pick <= df.iat[i,3]:
                  selectionResults.append(popRanked[i][0])
                  break
      return selectionResults

    def matingPool(population, selectionResults):
      matingpool = []
      for i in range(0, len(selectionResults)):
          index = selectionResults[i]
          matingpool.append(population[index])
      return matingpool

    def crossover(parent1, parent2):

      m1 = parent1[-1]
      m2 = parent2[-1]
      parent1 = parent1[1:-2]
      parent2 = parent2[1:-2]
      child = []
      childP1 = []
      childP2 = []

      geneA,geneB  = np.random.choice(range(0,len(parent1)),2,replace=False)
      startGene = min(geneA, geneB)
      endGene = max(geneA, geneB)

      #print(startGene,endGene)
      for i in range(startGene, endGene):
          childP1.append(parent1[i])

      childP2 = [item for item in parent2 if item not in childP1]

      child = childP1 + childP2
      if np.random.rand()<=0.5:
        m = m1
      else:
        m = m2

      child = ['Start'] + child + ['End'] + [m]
      return child

    def breedPopulation(matingpool, elite_percentage,crossover_rate ):
      eliteSize = int(len(matingpool)*elite_percentage)
      children = []
      length = len(matingpool) - eliteSize
      pool = random.sample(matingpool, len(matingpool))

      for i in range(0,eliteSize):
          children.append(matingpool[i])

      for i in range(0, length):
          if np.random.rand() <= 0.5:
            child = crossover(pool[i], pool[len(matingpool)-i-1])
          else:
            child = pool[i]
          children.append(child)
      return children

    def mutate(PL,verbose=False):

      li = PL.copy()
      p1,p2 = np.random.choice(range(1,len(li)-2),2,replace=False)
      p3 = np.random.choice([1,2],1)

      li[p1], li[p2] = li[p2], li[p1]

      li[-1] = p3[0]

      if verbose:
        print(f'index {p1} and index {p2} are swapped')
      return li

    def mutatePopulation(population, mutationRate,verbose=False):
      mutatedPop = []

      for ind in range(0, len(population)):
        if np.random.rand() <= mutationRate:
          mutatedInd = mutate(population[ind],verbose)
        else:
          mutatedInd = population[ind]
        mutatedPop.append(mutatedInd)
      return mutatedPop

    def nextGeneration(currentGen, elite_percentage,crossover_rate, mutationRate):

      popRanked = rankSchedules(currentGen)
      selectionResults = selection(popRanked, elite_percentage)
      matingpool = matingPool(currentGen, selectionResults)
      children = breedPopulation(matingpool,elite_percentage,crossover_rate)
      nextGeneration = mutatePopulation(children, mutationRate)
      return nextGeneration

    def geneticAlgorithm(PROJECT, popSize, elite_percentage = 0.2, crossover_rate = 0.2, mutationRate = 0.05, generations = 100,show=False,initial_solution = None):

      if show:
        iter_list = []
        z_list = []

      pop = initialPopulation(popSize, PROJECT,initial_solution)
      best_schedule = pop[0]
      best_obj = Fitness(best_schedule)

      if show:
        for i in range(generations):
          pop = nextGeneration(pop, elite_percentage,crossover_rate, mutationRate)
          best_generation = pop[0]
          best_obj_generation = Fitness(best_generation)
          if show:
            print(f'Generation {i}, best solution of generation {best_generation}, obj: {int(ph/best_obj_generation)}')
            print('-'*150)
          if best_obj_generation > best_obj:
            best_schedule, best_obj = best_generation, best_obj_generation
          if show:
            iter_list.append(i)
            z_list.append(int(ph/best_obj))
      if not show:
        for i in tqdm(range(generations),miniters=10,colour='green'):
          pop = nextGeneration(pop, elite_percentage,crossover_rate, mutationRate)
          best_generation = pop[0]
          best_obj_generation = Fitness(best_generation)
          if show:
            print(f'Generation {i}, best solution of generation {best_generation}, obj: {int(ph/best_obj_generation)}')
            print('-'*150)
          if best_obj_generation > best_obj:
            best_schedule, best_obj = best_generation, best_obj_generation
          if show:
            iter_list.append(i)
            z_list.append(int(ph/best_obj))


      if show:
        plt.plot(iter_list, z_list)
        plt.xlabel('Generations')
        plt.ylabel('Fitness Value')
        plt.show()

      return best_schedule

    if max_resources is None:
      max_resources = self.max_resources

    ph = sum(self.a_duration)

    if len(self.PROJECT) == 0:
      warnings.warn("!WARNING: Creating Project data dictionary...")
      self.create_project_dict()

    PROJECT = self.PROJECT

    EDGES = list(self.graph.edges)

    solution_pl = geneticAlgorithm(PROJECT, popSize, elite_percentage, crossover_rate, mutationRate, generations,show,initial_solution)

    method = solution_pl[-1]
    pl = solution_pl[:-1]

    if method == 1:
      mthd = 'SSG'
      schedule = self.SSG(pl,max_resources=max_resources,verbose=False,save=False)
      dur = schedule['End']['EF']
    if method == 2:
      mthd = 'PSG'
      schedule = self.PSG(pl,max_resources=max_resources,verbose=False,save=False)
      dur = schedule['End']['EF']

    best = {'PR':'GENETIC ALGORITHM','chromosome':pl,'schedule_method':mthd,'solution':schedule,'makespan':dur}

    if not hasattr(self,'best'):
      self.best = best

    if best['makespan'] < self.best['makespan']:
      self.best = best

    return best
  
  def calculate_project_cost(self,resource_costs,verbose = False,currency_sumbol = '€'):

    """
    Calculate the total project cost based on resource costs.

    This method calculates the project cost by multiplying the cost of each resource by the
    corresponding resource quantity and summing up these costs.

    Parameters
    ----------
    resource_costs : list of float
        A list containing the cost of each resource. The list length must match the number
        of resources in the project.

    verbose : bool, optional
        If True, detailed cost breakdown information will be printed for each resource.
        Default is False.

    currency_symbol : str, optional
        The symbol representing the currency used for displaying cost values. Default is '€'.

    Returns
    -------
    float
        The total project cost calculated based on the provided resource costs.

    Raises
    ------
    ValueError
        If the 'resource_costs' parameter is not a list or if its length does not match the
        number of resources in the project.

    Examples
    --------
    >>> resource_costs = [100.0, 200.0, 150.0]
    >>> project.calculate_project_cost(resource_costs, verbose=True)
    - Resource 1                    cost =    100.00 €
    - Resource 2                    cost =    200.00 €
    - Resource 3                    cost =    150.00 €

    Total project cost = 450.00 €
    """

    if not isinstance(resource_costs,list):
      raise ValueError('Sorry the resource cost must be a list with the cost of each resource')
    
    costs = np.array(self.a_resources).dot(resource_costs)
    self.a_cost = costs
    project_cost = costs.sum()

    if verbose:

      for a,c in zip(self.a_desc,self.a_cost):

        if a == 'Start of Project' or a == 'End of Project':
          continue

        print(f'- {a:<30} cost = {c:>10,.2f} {currency_sumbol}')
      
      print()
      print(f'Total project cost = {project_cost:,.2f} {currency_sumbol}')

    return project_cost

    
  @classmethod
  def from_cv_dataset_rcp_file(cls,file_name,verbose=False):

    archivo = open(file_name, mode = 'r', encoding = 'utf-8-sig')
    lines = archivo.readlines()

    has_empty_line = False
    empty_lines = []
    for i,line in enumerate(lines):
      if line.strip() == '':
        print('hey empty line, correcting it do not worry')
        has_empty_line = True
        empty_lines.append(i)

    for i in empty_lines:
      lines.pop(i)

    N,n_resources = list(map(int,lines[0].replace('      ',',').split(',')[0:-1]))
    max_resources_list = list(map(int,lines[1].replace('      ',',').split(',')[0:-1]))

    max_resources = dict()
    for i,r in enumerate(max_resources_list):
      res_name = f'resource_{i+1}'
      max_resources[res_name] = r

    end_node = str(N)
    if verbose:
      print(f'{file_name} Instance with {N} activities, Number of renewable resources = {n_resources}, max resources = {max_resources_list}')
      print()

    dummy_0 = lines[2].replace('      ',',').replace(' ','').split(',')
    start = 3
    if lines[3][0] == ' ':

      dummy_0 = dummy_0[:-1] + lines[3].replace('      ',',').replace(' ','').split(',')[:-1]
      start = 4
    else:
      dummy_0 = dummy_0[:-1]

    PROJECT_DATA = {'1':{'duration':int(dummy_0[0]),
                        'resources':dummy_0[1:1+n_resources],
                        'MAX_resources':max_resources_list,
                        'succesors':dummy_0[n_resources+2:]}}

    for i,r in enumerate(max_resources):
      PROJECT_DATA['1'][r] = int(PROJECT_DATA['1']['resources'][i])

    for i in range(start,len(lines)):

      info = lines[i].replace('      ',',').replace(' ','').split(',')[:-1]
      activity = {'duration':int(info[0]),
                  'resources':info[1:1+n_resources],
                  'MAX_resources':max_resources_list,
                  'succesors':info[n_resources+2:]}

      for j,r in enumerate(max_resources):
        activity[r] = int(activity['resources'][j])

      PROJECT_DATA[str(i+2 - start)] = activity

    predecessors = dict()
    for a1 in PROJECT_DATA:
      predecessors[a1] = list()
    for a1 in predecessors:
      for suc in PROJECT_DATA[a1]['succesors']:
        predecessors[suc].append(a1)
    predecessors

    last = str(len(PROJECT_DATA))
    for a in PROJECT_DATA:

      prec = predecessors[a]
      prec = [x if x != '1' else 'Start' for x in prec]
      succ = PROJECT_DATA[a]['succesors']
      succ = [x if x != last else 'End' for x in succ]
      resources = PROJECT_DATA[a]['resources']
      resources = [int(x) for x in resources]
      PROJECT_DATA[a]['succesors'] = succ
      PROJECT_DATA[a]['precedence'] = prec
      PROJECT_DATA[a]['resources'] = resources
    PROJECT_DATA['1']['precedence'] = None

    n = len(PROJECT_DATA)
    n_r = len(max_resources)
    activities = [x for x in PROJECT_DATA]
    activities[0] = 'Start'
    activities[-1] = 'End'
    description = [f'activity_{x}' for x in PROJECT_DATA]
    description[0] = "Start of the project"
    description[-1] = 'End of the project'
    durations = [PROJECT_DATA[x]['duration'] for x in PROJECT_DATA]
    cost = [0 for x in PROJECT_DATA]
    precedence = [PROJECT_DATA[x]['precedence']for x in PROJECT_DATA]
    resources = [PROJECT_DATA[x]['resources'] for x in PROJECT_DATA]

    EDGES = []
    for a,prec in zip(activities,precedence):
      if prec == None or prec == [None]:
        continue

      for pr in prec:
        if pr == None or pr == [None]:
          continue
        EDGES.append((pr,a))

    G = nx.DiGraph()
    G.add_nodes_from(activities)
    G.add_edges_from(EDGES)

    return cls(n_activities = n,n_resources = n_r,activities=activities,
               a_desc = description,a_duration = durations,a_cost = cost,a_precedence = precedence,
               a_resources = resources,max_resources = max_resources_list,G = G,dummies = True)
    
  
  @classmethod
  def from_rangen_1_rcp_file(cls,file_name,verbose=False):
    archivo = open(file_name, mode = 'r', encoding = 'utf-8-sig')
    lines = archivo.readlines()

    line_1 = lines[1].strip().split(" ")
    n_activities,n_resources = [int(x) for x in line_1 if x != ""]

    last = str(n_activities)
    
    max_resources = lines[2].strip().split(" ")
    max_resources = [int(x) for x in max_resources if x != ""]

    if verbose:
      print(f'{file_name} Instance with {n_activities} activities, Number of renewable resources = {n_resources}, max resources = {max_resources}')
      print()

    PROJECT_DATA = {}
    for i,line in enumerate(lines[4:]):
      data = line.strip().split(" ")
      data = [x for x in data if x!= ""]
      PROJECT_DATA[str(i+1)] = {'duration':data[0],
                              'resources':data[1:n_resources+1],
                              'MAX_resources':max_resources,
                              'succesors':data[n_resources+2:]}

    predecessors = dict()
    for a1 in PROJECT_DATA:
      predecessors[a1] = list()
    for a1 in predecessors:
      for suc in PROJECT_DATA[a1]['succesors']:
        predecessors[suc].append(a1)


    for a in PROJECT_DATA:

      prec = predecessors[a]
      prec = [x if x != '1' else 'Start' for x in prec]
      succ = PROJECT_DATA[a]['succesors']
      succ = [x if x != last else 'End' for x in succ]
      resources = PROJECT_DATA[a]['resources']
      resources = [int(x) for x in resources] 
      PROJECT_DATA[a]['succesors'] = succ
      PROJECT_DATA[a]['precedence'] = prec
      PROJECT_DATA[a]['resources'] = resources
    PROJECT_DATA['1']['precedence'] = None


    n = len(PROJECT_DATA)
    n_r = len(max_resources)
    activities = [x for x in PROJECT_DATA]
    activities[0] = 'Start'
    activities[-1] = 'End'
    description = [f'activity_{x}' for x in PROJECT_DATA]
    description[0] = "Start of the project"
    description[-1] = 'End of the project'
    durations = [int(PROJECT_DATA[x]['duration']) for x in PROJECT_DATA]
    cost = [0 for x in PROJECT_DATA]
    precedence = [PROJECT_DATA[x]['precedence']for x in PROJECT_DATA]
    resources = [PROJECT_DATA[x]['resources'] for x in PROJECT_DATA]

    EDGES = []
    for a,prec in zip(activities,precedence):
      if prec == None or prec == [None]:
        continue

      for pr in prec:
        if pr == None or pr == [None]:
          continue
        EDGES.append((pr,a))

    G = nx.DiGraph()
    G.add_nodes_from(activities)
    G.add_edges_from(EDGES)

    return cls(n_activities = n,n_resources = n_r,activities=activities,
               a_desc = description,a_duration = durations,a_cost = cost,a_precedence = precedence,
               a_resources = resources,max_resources = max_resources,G = G,dummies = True)
  

  def produce_outputs_for_MILP(self):

    n = self.n_activities -2
    p = self.a_duration
    ph = sum(p)
    c = list(self.max_resources)
    u = self.a_resources

    edges = self.graph.edges
    S = []
    for ed in edges:
      start,end = ed
      if start == 'Start':
        start = 1
      if end == 'End':
        end = n+2
      start = int(start)
      end = int(end)
      S.append([start-1,end-1])

    output = {'n':n,'p':p,'S':S,'u':u,'c':c,'ph':ph}

    return output
  
  def get_weak_forbidden_sets(self,verbose=False):

    n_r = self.n_resources
    n = self.n_activities
    c = list(self.max_resources)
    u = self.a_resources
    activities = self.activities

    IS = [[] for x in range(n_r)]

    for i in range(n_r):
      B = c[i]
      for a in range(n):
        if u[a][i] > (B/2):
          
          if verbose:
            print(f'* Activity {activities[a]}, resource consumption {i+1} = {u[a][i]}, max capcity = {B}.  {u[a][i]} > {B/2:0.2f}')
          IS[i].append(activities[a])


    for i in range(n_r):

      if len(IS[i]) < 2:
        if verbose:
          print(f'There is just one activity in the forbiddent set {i}. At least two activities are needed to stablish a constraint. The set will be substitued by the empty set []')
        IS[i] = []

    return IS

  @staticmethod
  def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

  @staticmethod
  def check_descendants_check_weight(Set,network_graph,resource_consumption,max_resources,start_idx_0 = True,verbose = False,set_str=False):

    if verbose:
      print('Currently Evaluating',Set)
    nodes = sorted(list(network_graph.nodes))[1:-1]
    for n1 in Set:
      for n2 in Set:
        if n1==n2:
          continue
        else:
          if n2 in nx.descendants(network_graph,n1):
            if verbose:
              print(Set,'contain descendants cannot be part of IS...')
              print('#'*120)
            return False

    if set_str:
      Set = [int(x) for x in Set]

    for i,BK in enumerate(max_resources):
      resources = resource_consumption[i]
      if start_idx_0:
        resources = [resources[x] for x in Set]
      elif not start_idx_0:
        resources = [resources[x-1] for x in Set]
      if verbose:
        print("resources:",resources)

      weights = 0
      l_s = len(Set)
      for j in range(l_s):
        weights +=  resources[j]
        if j != (l_s-1) and weights > BK:
          if verbose:
            print("Hey",Set,"total_weight",weights,"BK",BK)
            print('#'*120)
          return False
      if weights > BK:
        if verbose:
          print("Forbiddent Set",Set,"total_weight",weights,"BK",BK)
          print('#'*120)
        return True
    if verbose:
      print("HUuuu",Set,"total_weight",weights,"BK",BK)
      print('#'*120)

    return False

  @staticmethod
  def return_str_set_index_format(Set):

    out = [int(x)-1 for x in Set]
    return tuple(out)

  def get_minimal_forbidden_sets(self,verbose=False,start_idx_0=True,set_str=False,str_output = True):

    network_graph = self.graph
    nodes = list(network_graph.nodes)
    resource_consumption = self.a_resources
    resource_consumption = np.transpose(resource_consumption).tolist()
    max_resources = list(self.max_resources)
    power_set = self.powerset(nodes[1:-1])
    power_set = [x for x in power_set if len(x)> 1]
    Power_Set = []
    for x in tqdm(power_set):
      evaluation = self.check_descendants_check_weight(x,network_graph,resource_consumption,max_resources,start_idx_0=start_idx_0,verbose=verbose,set_str=set_str)
      if evaluation:
        if verbose:
          print(f'{x} added to Minimum Forbidden set')
        Power_Set.append(x)
    
    forbidden_sets = []
    for s in Power_Set:

      fobidden = True
      for st in forbidden_sets:
        ST = set(st)
        S = set(s)
        if ST.issubset(S):
          fobidden = False
          break
      if fobidden:
        forbidden_sets.append(s)
    
    if not str_output: # generate output in index format and not in str. Specially relevant for .rcp files
      forbidden_sets = [self.return_str_set_index_format(x) for x in forbidden_sets]

    return forbidden_sets
  
  @staticmethod
  def check_descendants_only(Set,network_graph,start_idx_0 = True,verbose = False,set_str=False):

    if verbose:
      print('Currently Evaluating',Set)
    nodes = sorted(list(network_graph.nodes))[1:-1]
    for n1 in Set:
      for n2 in Set:
        if n1==n2:
          continue
        else:
          if n2 in nx.descendants(network_graph,n1):
            if verbose:
              print(Set,' Contain descendants cannot be part of A...')
              #print('#'*120)
            return False
    if verbose:
      print(Set,' Does not contain descendants so it can be part of A...')
      #print('#'*120)
    return True

  @staticmethod
  def check_check_weight_only(Set,resource_consumption,max_resources,start_idx_0 = True,verbose = False,set_str=False):

    if verbose:
      print('Currently Evaluating',Set)

    if set_str:
      Set = [int(x) for x in Set]

    for i,BK in enumerate(max_resources):
      resources = resource_consumption[i]
      if start_idx_0:
        resources = [resources[x] for x in Set]
      elif not start_idx_0:
        resources = [resources[x-1] for x in Set]
      if verbose:
        print(" resources:",resources)

      weights = 0
      l_s = len(Set)
      for j in range(l_s):
        weights +=  resources[j]
        if j != (l_s-1) and weights > BK:
          if verbose:
            print(" Hey",Set,"total_weight",weights,"BK",BK)
            print(" Cannot be part of the feasible set A")
            #print('#'*120)
          return False
      if weights > BK:
        if verbose:
          print(" Forbiddent Set",Set,"total_weight",weights,"BK",BK)
          print(" Cannot be part of the feasible set A")
          #print('#'*120)
        return False
    if verbose:
      print(" HUuuu",Set,"total_weight",weights,"BK",BK)
      print(" Can be part of the feasible set A")
      #print('#'*120)
    return True

  def get_feasible_subset(self,verbose=False,start_idx_0=True,set_str = False,str_output=True):

    network_graph = self.graph
    nodes = list(network_graph.nodes)
    resource_consumption = self.a_resources
    resource_consumption = np.transpose(resource_consumption).tolist()
    max_resources = list(self.max_resources)
    power_set = self.powerset(nodes[1:-1])
    power_set = [x for x in power_set if len(x)> 1]
    Power_Set = []
    for x in tqdm(power_set):
      prece_evaluation = self.check_descendants_only(x,network_graph,start_idx_0=start_idx_0,verbose=verbose,set_str=set_str)
      if prece_evaluation:
        if verbose:
          print(f'{x} has no precedence constraint relations')
        resource_evaluation = self.check_check_weight_only(x,resource_consumption,max_resources,start_idx_0=start_idx_0,verbose=verbose,set_str=set_str)
        if resource_evaluation:
          if verbose:
            print(f'{x} does not violate the resource constraints')
          Power_Set.append(x)
      if verbose:
        print('#'*120)

    Power_Set.sort(key=lambda x: len(x), reverse=True)


    if verbose:
      print()
      print('Getting maximum feasible sets A, removing subsets')
      print()
    # Initialize a list to store the result
    result = []

    # Iterate through the sorted list and add non-subset tuples to the result
    for tup in Power_Set:
        is_subset = False
        for existing_tup in result:
            if set(tup).issubset(existing_tup):
                is_subset = True
                if verbose:
                  print(f" set {tup} removed from A becase is a subset")
                break
        if not is_subset:
            if verbose:
              print(f" set {tup} included in A becase is not a subset")
            result.append(tup)
    
    if not str_output:
      result = [self.return_str_set_index_format(x) for x in result]

    return result

  def get_naive_graph_ES_EC_LS_LC(self,ph = None,verbose = True):

    if len(self.PROJECT) == 0:
      warnings.warn("!WARNING: Creating Project data dictionary...")
      self.create_project_dict()
    
    if ph == None:
      ph = sum(self.a_duration)
    
    PROJECT = self.PROJECT
    G = self.graph

    output = dict()
    for a in PROJECT:

      if verbose:
        print('Current activity:',a)

      if a == 'Start':
        output[a] = {'ES':0,'EC':0,'LS':0,'LC':0}
        if verbose:
          print(output[a])
          print('-'*120)
        continue
      if a == 'End':
        output[a] = {'ES':ph,'EC':ph,'LS':ph,'LC':ph}
        if verbose:
          print(output[a])
        continue
      
      start_paths = nx.all_simple_paths(G,'Start',a)
      max_start_path = None
      max_start_dist = 0

      for path in start_paths:

        path_d = [PROJECT[x]['duration'] for x in path]
        path_D = sum(path_d)
        if verbose:
          print(path,path_d,path_D)
        if path_D > max_start_dist:
          max_start_path = path
          max_start_dist = path_D
      if verbose:
        print(f'Max start path: {max_start_path} with distance {max_start_dist}')
      
      EC = max_start_dist
      ES = EC - PROJECT[a]['duration']

      end_paths = nx.all_simple_paths(G,a,'End')
      max_end_path = None
      max_end_dist = 0

      for path in end_paths:

        path_d = [PROJECT[x]['duration'] for x in path]
        path_D = sum(path_d)
        if verbose:
          print(path,path_d,path_D)
        if path_D > max_end_dist:
          max_end_path = path
          max_end_dist = path_D
      if verbose:
        print(f'Max end path: {max_end_path} with distance {max_end_dist}')
      
      LS = ph - max_end_dist
      LC = LS + PROJECT[a]['duration']

      output[a] = {'ES':ES,'EC':EC,'LS':LS,'LC':LC}
      if verbose:
        print(output[a])
        print('-'*120)
    
    return output