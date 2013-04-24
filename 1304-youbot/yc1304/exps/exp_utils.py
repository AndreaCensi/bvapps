


def iterate_context_episodes(context, episodes):
    """ Yields context, id_episode,  """
    for id_episode in episodes:
        name = id_episode.replace('-', '')
        e_c = context.child(name)
        yield e_c, id_episode


def iterate_context_agents(context, agents):
    """ Yields context, id_agent,  """
    for id_agent in agents:
        name = id_agent.replace('-', '')
        e_c = context.child(name)
        yield e_c, id_agent



def iterate_context_explogs(context, explogs):
    """ Yields context, id_agent,  """
    for id_explog in explogs:
        name = id_explog.replace('-', '')
        e_c = context.child(name)
        yield e_c, id_explog



def iterate_context_agents_and_episodes(context, agents, episodes):
    """ Yields context, id_agent, id_episode  """
    for cc, id_agent in iterate_context_agents(context, agents):
        for c, id_episode in iterate_context_episodes(cc, episodes):
            yield c, id_agent, id_episode


