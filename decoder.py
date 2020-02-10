# https://github.com/githubharald/CTCWordBeamSearch c++

import alphabet
import beam_entry
import beam_state
import decorators
import probabilities_array
import utils


class Decoder:
    """
    decoder without lm
    """

    def __init__(self) -> None:
        super().__init__()

    def _add_beam(self, beam_state, labeling):
        "add beam if it does not yet exist"
        if labeling not in beam_state.entries:
            beam_state.entries[labeling] = beam_entry.BeamEntry()

    @decorators.timing
    def beam_search(self, mat, classes, beam_width=25):
        "beam search as described by the paper of Hwang et al. and the paper of Graves et al."
        self._check_input_data(mat, classes)
        blankIdx = len(classes)
        maxT, maxC = mat.shape

        # initialise beam state
        last = beam_state.BeamState()
        labeling = ()
        last.entries[labeling] = beam_entry.BeamEntry()
        last.entries[labeling].prBlank = 1
        last.entries[labeling].prTotal = 1

        # go over all time-steps
        for t in range(maxT):
            curr = beam_state.BeamState()

            # get beam-labelings of best beams
            best_labelings = last.sort()[0:beam_width]

            # go over best beams
            for labeling in best_labelings:

                # probability of paths ending with a non-blank
                prNonBlank = 0
                # in case of non-empty beam
                if labeling:
                    # probability of paths with repeated last char at the end
                    prNonBlank = last.entries[labeling].prNonBlank * mat[t, labeling[-1]]

                # probability of paths ending with a blank
                prBlank = (last.entries[labeling].prTotal) * mat[t, blankIdx]

                # add beam at current time-step if needed
                self._add_beam(curr, labeling)

                # fill in data
                curr.entries[labeling].labeling = labeling
                curr.entries[labeling].prNonBlank += prNonBlank
                curr.entries[labeling].prBlank += prBlank
                curr.entries[labeling].prTotal += prBlank + prNonBlank
                curr.entries[labeling].prText = last.entries[
                    labeling].prText  # beam-labeling not changed, therefore also LM score unchanged from
                curr.entries[
                    labeling].lmApplied = True  # LM already applied at previous time-step for this beam-labeling

                # extend current beam-labeling
                for c in range(maxC - 1):
                    # add new char to current beam-labeling
                    newLabeling = labeling + (c,)

                    # if new labeling contains duplicate char at the end, only consider paths ending with a blank
                    if labeling and labeling[-1] == c:
                        prNonBlank = mat[t, c] * last.entries[labeling].prBlank
                    else:
                        prNonBlank = mat[t, c] * last.entries[labeling].prTotal

                    # add beam at current time-step if needed
                    self._add_beam(curr, newLabeling)

                    # fill in data
                    curr.entries[newLabeling].labeling = newLabeling
                    curr.entries[newLabeling].prNonBlank += prNonBlank
                    curr.entries[newLabeling].prTotal += prNonBlank

            # set new beam state
            last = curr

        # normalise LM scores according to beam-labeling-length
        last.norm()

        # sort by probability
        bestLabeling = last.sort()[0]  # get most probable labeling

        # map labels to chars
        res = ''
        for l in bestLabeling:
            res += classes[l]
        return res

    def _check_input_data(self, mat, classes):
        #TODO mat must be numpy array!because use mat.shape


        for one_timestep_probability in mat:
            # len probs[i] must be equal to len-1 alphabet
            assert len(one_timestep_probability) - 1 == len(classes)
            # sum of probs on random timestep must be <=1,
            # in test2 probs[1,2,3] we have many strings with sum(probs)>1(1.01 for example)
            # assert sum(one_timestep_probability) <= 1
            # print(sum(one_timestep_probability))



if __name__ == '__main__':
    decoder = Decoder()
    prob_list, alphabet_list = utils.parse_arguments()
    probabilities_obj = probabilities_array.ProbabilitiesArray(prob_list)
    alphabet_obj = alphabet.Alphabet(alphabet_list)
    # print(f"prob list: {prob_list}, alphabet: {alphabet_obj.alphabet}")

    res = decoder.beam_search(probabilities_obj.probabilities_np, alphabet_obj.alphabet)
    print(f"result: {res}")
