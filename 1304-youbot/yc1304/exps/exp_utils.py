


def iterate_context_episodes(context, episodes):
    """ Yields context, id_episode,  """
    for id_episode in episodes:
        name = id_episode.replace('-', '')
        e_c = context.child(name)
        yield e_c, id_episode
