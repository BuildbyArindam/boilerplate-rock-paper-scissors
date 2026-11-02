# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import random

BEAT = {"R": "P", "P": "S", "S": "R"}
state = {"my": [], "opp": [], "scores": {}, "preds": {}}


def most_common(seq):
    return max(set(seq), key=seq.count)


def ngram_predict(opp, k):
    """Predict the opponent's next move from what followed the same last-k moves before."""
    if len(opp) <= k:
        return None
    ctx = opp[-k:]
    followers = [opp[i + k] for i in range(len(opp) - k) if opp[i:i + k] == ctx]
    return most_common(followers) if followers else None


def predict_kris(my, opp):
    return BEAT[my[-1]] if my else None


def predict_mrugesh(my, opp):
    if not my:
        return None
    return BEAT[most_common(my[-10:])]


def predict_abbey(my, opp):
    hist = ["R"] + my
    if len(hist) < 2:
        return None
    pairs = {a + b: 0 for a in "RPS" for b in "RPS"}
    for i in range(len(hist) - 1):
        pairs[hist[i] + hist[i + 1]] += 1
    last = hist[-1]
    options = [last + "R", last + "P", last + "S"]
    guess = max(options, key=lambda k: pairs[k])[-1]
    return BEAT[guess]


def predict_quincy(my, opp):
    return ngram_predict(opp, 2)


PREDICTORS = {
    "kris": predict_kris,
    "mrugesh": predict_mrugesh,
    "abbey": predict_abbey,
    "quincy": predict_quincy,
    "opp_order3": lambda my, opp: ngram_predict(opp, 3),
}


def player(prev_play, opponent_history=[]):
    my, opp = state["my"], state["opp"]

    if prev_play == "":
        my.clear()
        opp.clear()
        state["scores"] = {name: 0.0 for name in PREDICTORS}
        state["preds"] = {}
        guess = random.choice(["R", "P", "S"])
        my.append(guess)
        return guess

    opp.append(prev_play)
    for name, pred in state["preds"].items():
        hit = 1.0 if pred == prev_play else 0.0
        state["scores"][name] = 0.9 * state["scores"][name] + hit

    preds = {}
    for name, fn in PREDICTORS.items():
        p = fn(my, opp)
        if p is not None:
            preds[name] = p
    state["preds"] = preds

    if preds:
        best = max(preds, key=lambda n: state["scores"][n])
        move = BEAT[preds[best]]
    else:
        move = random.choice(["R", "P", "S"])

    my.append(move)
    return move