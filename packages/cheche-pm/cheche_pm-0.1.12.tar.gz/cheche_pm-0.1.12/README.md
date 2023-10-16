# cheche_pm - Project Scheduling Toolkit

A Python package for project scheduling, designed to simplify project management tasks.

## Table of Contents

- [Installation](#installation)
- [Usage](##usage)
  - [Create project](###Create_project)
  - [from_csv](###from_csv)
  - [CPM](###cpm)
  - [Priority List](###priority_list)
  - [Scheduling methods](###Scheduling_methods)
  - [Genetic Algorithm](###Genetic_Algorithm)
  - [Risk Analysis](###Risk_Analysis)
- [Contributor](##contributor)
- [License](##license)

## Installation

To install `cheche_pm`, you can use pip:

```bash
pip install cheche_pm
```

## Usage
To use cheche_pm, import the Project class and start utilizing its methods. Here are some of the key methods provided by the package:


### Create project

creates an empty project. Activities can be added manually.

```python
from cheche_pm import Project

p = p.Project()

p.add_activity(activity_name='A',activity_duration=2,activity_precedence = [None], activity_resources= [2,4,5])
p.add_activity(activity_name='B',activity_duration=3,activity_precedence =['A'],activity_resources= [3,7,8])
p.add_activity(activity_name='C',activity_duration=4,activity_precedence =['B'],activity_resources=[3,2,2])
p.add_activity(activity_name='D',activity_duration=3,activity_precedence =['A'],activity_resources=[4,5,6])
```

Activities can be also deleted.

```python
p.delete_activity('D')
```

Once the activities are created the user, can add the terminal dummy nodes. "Start" and "End" by using the following methods.

```python
p.add_dummies_create_project_network()
```

### from_csv or from_excel

A project can be created from a .csv file or .xlsx file. Imagine that we have an MS EXCEL file with the data below

| Activity | Description  | Duration | Precedence | Cost  | Bulbasaur | Charizard | Squirtle |
|----------|--------------|----------|------------|-------|-----------|-----------|----------|
| A        | F.House      | 5        |            | 1000  | 1         | 0         | 0        |
| B        | F.Pool       | 2        |            | 2000  | 1         | 0         | 0        |
| C        | Walls        | 5        | A          | 3500  | 0         | 1         | 0        |
| D        | Pool         | 6        | B          | 4500  | 0         | 0         | 1        |
| E        | Roof         | 5        | C          | 2600  | 0         | 1         | 0        |
| F        | Windows      | 2        | C          | 7000  | 0         | 1         | 0        |
| G        | Electricity  | 3        | C          | 8000  | 0         | 0         | 1        |
| H        | S.Panels     | 2        | E          | 1000  | 0         | 0         | 1        |
| I        | Plumbing     | 4        | F          | 5600  | 0         | 0         | 1        |
| J        | Finishings   | 3        | H, I       | 12000 | 0         | 0         | 1        |

A project can be created using the following methods:

#### .csv file


```python
p = Project.from_csv(filename='data_project.csv',rcpsp_format=True,n_resources= 3,max_resources=[1,1,1])

```

#### .xlsx file

``` python
p = Project.from_excel(filename='data_project.xlsx',rcpsp_format=True,n_resources= 3,max_resources=[1,1,1])
```
### CPM

This method allows the generation of project schedule using the critical path method

```python
p.CPM()

```

the user can ask for the critical path

```python
p.get_critical_path()
```

### priority_list

This method allows the user to generate a priority list from a given priority rule:

- **LPT:** Longest processing time
- **SPT:** Shortest processing time
- **LIS:** Least immediate successors
- **MIS:** Most immediate successor
- **LTS:** Least total successors
- **MTS:** Most total successors
- **sEST:** Smallest Earliest Start Time
- **gEST:** Greatest Earliest Start Time
- **sEFT:** Smallest Earliest Finish Time
- **gEFT:** Greatest Earliest Finish Time
- **sLST:** Smallest Latest Start Time
- **gLST:** Greatest Latest Start Time
- **sLFT:** Smallest Latest Finish Time
- **gLFT:** Greatest Latest Finish Time
- **MINF:** Minimum float
- **MAXF:** Maximum float
- **GRPW:** Greatest GRPW
- **LRPW:** Lowest GRPW
- **FCFS:** First comes first served
- **LCFS:** Last comes first served
- **GRD:** Greatest resource demand
- **LRD:** Lowest resource demand
- **GCRD:** Greatest cumulative resource demand
- **LCRD:** Lowest cumulative resource demand

The user can ask for an individual priority list.

```python
PL = p.get_priority_list(priority_rule= 'FCFS',verbose=True,save=True)
```

### Scheduling_methods

Once the user has a priority list it can decide to produce an schedule from it. The user can generate a serial schedule (SSG) or a parallel one (PSG)

#### Serial (SSG)
```python
ssg = p.SSG(PL,max_resources=[1,1,1],verbose=False)
```

#### Parallel (PSG)
```python
psg = p.PSG(PL,max_resources=[1,1,1],verbose=False)
```
The user can also decide to run all priority list heuristics, and schedule each one via the two methods. This method will return the best schedule obtained.

```python
p.run_all_pl_heuristics()
```
#### Visualizations of schedules

Once an schedule is produced, the user can ask for a datetime schedule by providing the date for the project start.

```python
w_sche = p.generate_datetime_schedule(solution = ssg,start_date="2023-09-03",weekends_work=False,max_resources=[1,1,1],verbose=True)
```

The user can then ask for a gantt chart of this datetime schedule

```python
p.plot_date_gantt(w_sche)
```

The user can ask for the critical chain of this schedule

```python
p.get_critical_chain(ssg,max_resources=[1,1,1])
```

The user can perform resource vistualizations

```python
p.plot_resource_levels(ssg)
```

```python
p.RCPSP_plot(ssg,resource_id=0)
```


### Genetic_Algorithm

The user can use the genetic algorithm optimization method to find the optimal schedule.

```python
p.genetic_algorithm_optimization(popSize = 40, elite_percentage = 0.2, crossover_rate = 0.5, mutationRate = 0.5, generations = 100,show = True)
```

### Risk analysis
These methods offers a collection of monte carlo simulation methods, that can be used to evaluate project makespan uncertainty as well as the effectivenes of activity buffers.

#### Simple Monte Carlo simulation
```python
p.monte_carlo_cpm_simple(optimistic=0.25,pessimistic=1)
```

#### Detailed Monte Carlo simulation

```python
pessimistic = {'A':7.5,'B':3.5,'C':7.5,'D':9,'E':7.5,'F':3,'G':4.5,'H':3,'I':6,'J':4.5}
optimistic = {'A':2.5,'B':1,'C':2.5,'D':3,'E':2.5,'F':1,'G':1.5,'H':1,'I':2,'J':1.5}

p.monte_carlo_cpm_detailed(optimistic=optimistic,pessimistic=pessimistic, NumberIterations=1000)
```

#### Buffer analysis


```python
pessimistic = {'A':7.5,'B':3.5,'C':7.5,'D':9,'E':7.5,'F':3,'G':4.5,'H':3,'I':6,'J':4.5}
optimistic = {'A':2.5,'B':1,'C':2.5,'D':3,'E':2.5,'F':1,'G':1.5,'H':1,'I':2,'J':1.5}
buffer = {'A':2,'C':2,'E':3,'H':2,'F':2,'I':1,'J':2}

p.monte_carlo_detail_buffer_analysis(optimistic=optimistic,pessimistic=pessimistic,buffer=buffer, NumberIterations=2000)
```

## Contributors
Author: **Luis Fernando Perez Armas**

Email: luisfernandopa1212@gmail.com

LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/luis-fernando-perez-project-manager/)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

**MIT License**

Copyright (c) 2023, Luis Fernando Pérez Armas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.