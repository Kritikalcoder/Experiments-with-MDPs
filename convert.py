
states_count = int ( raw_input (" Enter states count: "))
joint_actions_count = int ( raw_input (" Enter joint actions count: "))
agent_count = int ( raw_input (" Enter number of agents: "))
resources_count = int ( raw_input ( " Enter number of resources: ") )

states = [0 for x in range(states_count)]
joint_actions = [[0 for x in range(agent_count)] for y in range(joint_actions_count)] 
reward = [[0 for x in range(joint_actions_count)] for y in range(states_count)] 
comm = [[0 for x in range(joint_actions_count)] for y in range(states_count)] 
trans = [[[0 for x in range(states_count)] for y in range(joint_actions_count)] for z in range(states_count) ] 
cost1 = [[[0 for x in range(resources_count)] for y in range(joint_actions_count)] for z in range(states_count) ]
cost2 = [[[0 for x in range(resources_count)] for y in range(joint_actions_count)] for z in range(states_count) ]
comm_threshold = [[0 for x in range(joint_actions_count)] for y in range(states_count)] 

#Assuming a two agent system
threshold1 = [0 for x in range(resources_count)]
threshold2 = [0 for x in range(resources_count)]

print "Enter states \n"
for i in range ( states_count ) :
	states [i] = raw_input (str(i) + "> ")

print "Enter joint actions \n"
for i in range ( joint_actions_count ) :
	joint_actions [i][0] = raw_input (str(i) + ",0 >" )
	joint_actions [i][1] = raw_input (str(i) + ",1 >" )

for index1, source in enumerate(states):
	for index2, a_row in enumerate(joint_actions):
		print ( "Enter reward for ")
		reward [ index1 ][ index2 ] = raw_input ( "( " + str(source) + ", " + str(a_row)+ ") : " )
		print ( "Enter joint communication costs for ")
		comm [ index1 ][ index2 ] = raw_input ( "( " + str(source) + ", " + str(a_row) + ") : " )
		for index3, dest in enumerate(states):
			print ( "Enter transition probability for ")
			trans [ index1 ][ index2 ][ index3 ] = raw_input ( "( " + str(source) + ", " + str(a_row) + ", " + str(dest) + ") : " )
		for r in range ( resources_count ):
			cost1 [ index1 ][ index2 ][ r ] = raw_input ( " Enter cost of resource for agent 1 for ( " + str(source) + ", " + str(a_row)  + ", " + str(r) + ") : ")
			cost2 [ index1 ][ index2 ][ r ] = raw_input ( " Enter cost of resource for agent 2 for ( " + str(source) + ", " + str(a_row) + ", " + str(r) + ") : ")
		comm_threshold [ index1 ][ index2 ] = raw_input ( " Enter joint communication cost threshold for ( " + str(source) + ", " + str(a_row) + "): ")


print ( "Enter resource thresholds:\n " )
for r in range ( resources ):
	print ( "Resource " + r + ":\n")
	threshold1 [r] = raw_input (" Agent 1 >")
	threshold2 [r] = raw_input (" Agent 2 >")	

conversion ( states, states_count, joint_actions, joint_actions_count, trans, reward, cost1, cost2, threshold1, threshold2, comm, comm_threshold )

def conversion ( s, s_count, a, a_count, p, r, c1, c2, t1, t2, n, q ) :
	#initialize
	s_new = s
	a_new = a
	p_new = p
	r_new = [[0 for x in range(joint_actions_count)] for y in range(states_count)]
	c1_new = [[[0 for x in range(resources_count)] for y in range(joint_actions_count)] for z in range(states_count) ]
	c2_new = [[[0 for x in range(resources_count)] for y in range(joint_actions_count)] for z in range(states_count) ]
	t1_new = t1
	t2_new = t2
	n_new = [[0 for x in range(joint_actions_count)] for y in range(states_count0)]
	q_new = q
	Pf = 0

	for index1, source in enumerate(s) :
		for index2, action_row in enumerate(a) :
			sa_nc = source + " " + action_row[0] + " nc"
			a_nc = [ action_row[0] + " nc", "" ]
			if sa_nc not in s_new :
				[ new_index_state_nc, new_index_action_nc ] = SrcToComm ( index1, source, index2, action_row, sa_nc, a_nc, s_count, a_count, s_new, a_new, r_new, c1_new, n_new  )
				#new_index is for sa_nc, a_nc
				p_new [ index1 ][ index2 ][ new_index_state_nc ] = 1
				counter = 0
				for a_index, a_ctr in enumerate(a) :
					#if a_ctr[0] == action_row[0] :
					if a_index == index2 :
						for dest_index, dest in enumerate(s):
							if ( p [ index1 ][ a_index ][ dest_index ] > 0 ):  
								counter = counter + 1
				if counter > 1 :
					sa_c = source + " " + action_row[0] + " c"
					a_c = [ action_row[0] + " c", "" ]
					[ new_index_state_c, new_index_action_c ] = SrcToComm ( index1, source, index2, action_row, sa_c, a_c, s_count, a_count, s_new, a_new, r_new, c1_new, n_new  )
					n_new [ index1 ][ new_index_action_c ] = 1
					p_new [ index1 ][ new_index_action_c ][ new_index_state_c ] = 1 - Pf
					p_new [ index1 ][ new_index_action_c ][ new_index_state_nc ] = Pf

			if index2 == 1 :
				conditional_prob_value = prob [ action_row[1] ][ new_index_state_nc ]
				# still need to calculate this value
			else:
				prob [ action_row[1] ][ new_index_state_nc ] = conditional_prob_value

			CommToDest ( index1, source, index2, action_row, new_index_state_nc, sa_nc, new_index_action_nc, a_nc, p_new, r_new, c1_new, c2_new, p, r, c1, c2 )

			counter = 0
			for a_index, a_ctr in enumerate(a) :
				#if a_ctr[0] == action_row[0] :
				if a_index == index2 :
					for dest_index, dest in enumerate(s):
						if ( p [ index1 ][ a_index ][ dest_index ] > 0 ):  
							counter = counter + 1
			if counter > 1 :
				CommToDest ( index1, source, index2, action_row, new_index_state_c, sa_c, new_index_action_c, a_c, p_new, r_new, c1_new, c2_new, p, r, c1, c2 )

			for index3, state_new in enumerate(s_new) :
				p_new [ index1 ][ index2 ][ index3 ] = 0


def SrcToComm (s_index, s_parent, a_index, a_parent, s_current, a_current, s_count, a_count, s_new, a_new, r_new, c1_new, n_new ) :
	if s_current not in s_new :
		s_count = s_count + 1
		s_new.append ( s_current )
		s_current_index = len(s_new) - 1
		print " adding state "
	else:
		for index, s in s_new:
			if s_current == s:
				s_current_index = index
	if a_current not in a_new:
		a_count = a_count + 1
		#add a_current to a_new
		a_new.append ( a_current )
		a_current_index = len(a_new) - 1
		#a_current_index ??
		print " adding action "
	else:
		for index, a in a_new:
			if a_current == a:
				a_current_index = index
	r_new [ s_index, a_current_index ] = 0
	c1_new [ s_index, a_current_index ] = 0 
	c2_new [ s_index, a_current_index ] = 0
	n_new [ s_index, a_current_index ] = 0
	return [ s_current_index, a_current_index ]
	#new state index ????


def CommToDest (s_index, s_parent, a_index, a_parent, sc_index, s_current, ac_index, a_current, p_new, r_new, c1_new, c2_new, p, r, c1, c2 ) :
	for state_index, state in s_new :
		p_new [ sc_index, a_index, state_index ] = p [ s_index, a_index, state_index ]
	r_new [ sc_index, a_index ] = r [ s_index, a_index ]
	c1_new [ sc_index, a_index ] = c1 [ s_index, a_index ]
	c2_new [ sc_index, a_index ] = c2 [ s_index, a_index ]
