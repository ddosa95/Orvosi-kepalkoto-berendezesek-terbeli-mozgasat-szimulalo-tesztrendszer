from adapter.classes import WorldHandler, Visualizer

PART_LIST_JSON = "adapter\spect_ct.json"


def main():
    simulation = WorldHandler.WorldHandler()
    simulation.load_part_list(PART_LIST_JSON)

    three_d_sim = Visualizer.Visualizer()

    while three_d_sim.is_running:
        if simulation.simulation_is_running:
            simulation.tick()
        three_d_sim.render(simulation)


if __name__ == '__main__':
    main()
