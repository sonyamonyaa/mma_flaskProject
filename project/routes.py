import logging
import os
from flask import render_template, request, flash, redirect, url_for, get_flashed_messages
from project import app
from project.forms import InputForm
from fairpyx import divide, Instance
from project import maximin_aware as mma
import random

@app.route('/', methods=['GET', 'POST'])
def index():
    # Init. input form with some example values
    input_form = InputForm(algo_name='', participants='Alice, Bob, Claire', items='Item1, Item2, Item3, Item4')

    participants = []
    items = []
    algo_name = ''
    random_values = {}

    if input_form.validate_on_submit():
        algo_name = input_form.algo_name.data
        participants = [p.strip() for p in input_form.participants.data.split(',') if p.strip()]
        items = [i.strip() for i in input_form.items.data.split(',') if i.strip()]

        if request.form.get('generate_random'):
            random_values = {participant: {item: random.randint(1, 100) for item in items} for participant in participants}

        if algo_name == '':
            flash('Please select an algorithm', category='danger')
        elif not (2 <= len(participants) <= 6):
            flash('Put between 2 and 6 participants', category='danger')
        elif not (2 <= len(items) <= 15):
            flash('Put between 2 and 15 items', category='danger')
        elif algo_name == 'div' and len(participants) != 3:
            flash('You must put 3 participants to use Divide and Choose', category='danger')
        elif (2 <= len(items) <= 15) and (2 <= len(participants) <= 6):
            flash('Please put below valuations of each', category='success')

        errors = get_flashed_messages(category_filter=['danger'])

        # Only proceed if there are no errors
        if errors:
            participants = []
            items = []
            algo_name = ''

        # For debugging: Output the participants and items
        # print(f"Participants: {participants}")
        # print(f"Items: {items}")
        # print(f"Algo name: {algo_name}")

    return render_template('index.html', input_form=input_form, participants=participants,
                           items=items, algo_name=algo_name, random_values=random_values)


# Route for submitting the values for each participant and their items
@app.route('/output', methods=['POST'])
def submit():
    algo_name = request.form.get('algo_name')
    participants = [p for p in request.form.get('participants').split(',')]
    print(f"participants {participants}")
    items = [i for i in request.form.get('items').split(',')]
    print(f"items {items}")
    submitted_data = {}
    total_value = 0
    for participant in participants:
        participant_total = 0
        submitted_data[participant] = {}
        for item in items:
            field_name = f'{participant}_{item}'
            res = request.form.get(field_name)
            value = 0 if res is None else int(res)

            submitted_data[participant][item] = value
            participant_total += value

        if participant_total == 0:
            flash(
                f'All Values for {participant} are 0, either add valuations or remove {participant} from participants',
                category='danger')
            return redirect(f"{url_for('index')}#form-section")
    # For debugging: Output the received submitted_data
    # print(f" submitted_data {submitted_data}")
    if algo_name == 'div':
        allocation, logs = get_allocation(algorithm=mma.divide_and_choose_for_three, valuations=submitted_data,
                                    participants=participants)
    elif algo_name == 'alloc':
        allocation, logs = get_allocation(algorithm=mma.alloc_by_matching, valuations=submitted_data,
                                    participants=participants)
    else:
        allocation, logs = {}, {}

    return render_template('output.html', algo_name=algo_name, submitted_data=submitted_data,
                           allocation=allocation, logs=logs)


def get_allocation(algorithm: callable, valuations: dict[str, dict[str, str]], participants: list):
    import numpy as np
    from fairpyx import explanations, AgentBundleValueMatrix
    logger = explanations.StringsExplanationLogger(agents=participants, level=logging.INFO)
    instance = Instance(valuations=valuations)
    result = divide(algorithm=algorithm, instance=instance, explanation_logger=logger)
    allocation = {participant: {'items': items, 'value': instance.agent_bundle_value(participant, result[participant])}
                  for participant, items in result.items()}

    logs = logger.map_agent_to_explanation()

    for agent, log in logs.items():
        absolute_value = instance.agent_bundle_value(agent, result[agent])
        maximum_value = instance.agent_maximum_value(agent) / instance.num_of_agents
        relative_value = absolute_value / maximum_value * 100
        true_capacity = int(np.ceil(instance.num_of_items/instance.num_of_agents))
        new_summary = (f'\nIn term of item allocation, your bundle is worth {int(np.round(relative_value))}% of the average value '
                       f'of {true_capacity} items.')
        logs[agent] += new_summary
    return allocation, logs
