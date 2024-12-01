tasks = ['guitar', 'shoes', 'gym', 'food']

print(f'Number of tasks: {len(tasks)}')

print(f'Tasks: {tasks}')

print(f'Alphabetical order: {sorted(tasks)}')

print('Adding...')
new_task = 'python'
tasks.append(new_task)
new_task = 'water'
tasks.insert(2, new_task)

print(f'Tasks list: {tasks}')

tasks.sort()
print(f'Final lists (alphabetical order): {tasks}')
