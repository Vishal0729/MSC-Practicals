from neurodynex.hopfield_network import network, pattern_tools, plot_tools
pattern_size=5
hopfield_net=network.HopfieldNetwork(nr_neurons=pattern_size**2)
factory=pattern_tools.PatternFactory(pattern_size,pattern_size)
checkerboard=factory.create_checkerboard()
pattern_list=[checkerboard]
pattern_list.extend(factory.create_random_pattern_list(nr_patterns=3,on_probability=0.5))
plot_tools.plot_pattern_list(pattern_list)
overlap_matrix=pattern_tools.compute_overlap_matrix(pattern_list)
plot_tools.plot_overlap_matrix(overlap_matrix)
hopfield_net.store_patterns(pattern_list)
noisy_init_state=pattern_tools.flip_n(checkerboard,nr_of_flips=4)
hopfield_net.set_state_from_pattern(noisy_init_state)
states=hopfield_net.run_with_monitoring(nr_steps=4)
states_as_patterns=factory.reshape_patterns(states)
plot_tools.plot_state_sequence_and_overlap(states_as_patterns,pattern_list,reference_idx=0,suptitle="Network dynamics")
