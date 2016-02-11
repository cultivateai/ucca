import os

import numpy as np

import parser.parser
from parser.config import Config
from ucca.evaluation import UNLABELED, WEAK_LABELED, LABELED


class Hyperparams(object):
    def __init__(self, learning_rate, decay_factor):
        self.learning_rate = learning_rate
        self.decay_factor = decay_factor
        self.scores = None

    def run(self):
        assert Config().args.train and Config().args.passages or Config().args.folds, \
            "insufficient parameters given to parser"
        print("Running with %s" % self)
        Config().learning_rate = self.learning_rate
        Config().decay_factor = self.decay_factor
        self.scores = parser.main()
        assert self.score is not None, "parser failed to produce score"

    def score(self):
        return -float("inf") if self.scores is None else self.scores.average_f1()

    def __str__(self):
        ret = "learning rate: %.3f" % self.learning_rate
        ret += ", decay factor: %.3f" % self.decay_factor
        if self.scores is not None:
            ret += ", average f1: %.3f" % self.score()
        return ret

    def print(self, file):
        e = self.scores.evaluators
        print(", ".join("%.3f" % p for p in
                        [self.learning_rate, self.decay_factor, self.score(),
                         e[LABELED].regular.f1,      e[LABELED].remotes.f1,
                         e[UNLABELED].regular.f1,    e[UNLABELED].remotes.f1,
                         e[WEAK_LABELED].regular.f1, e[WEAK_LABELED].remotes.f1]),
              file=file)

    @staticmethod
    def print_title(file):
        print("learning rate, decay factor, average f1, "
              "regular labeled f1, remote labeled f1, "
              "regular unlabeled f1, remote unlabeled f1, "
              "regular weakly labeled f1, remote weakly labeled f1, ",
              file=file)


def main():
    out_file = os.environ.get("HYPERPARAMS_FILE", "hyperparams.csv")
    num = int(os.environ.get("HYPERPARAMS_NUM", 30))
    dims = (num, 2)
    hyperparams = list(set(
        Hyperparams(learning_rate, decay_factor)
        for learning_rate, decay_factor in
        np.round(0.001 + np.random.exponential(0.8, dims), 3)
    ))
    print("\n".join(["All hyperparam combinations to try: "] +
                    [str(h) for h in hyperparams]))
    print("Saving results to '%s'" % out_file)
    with open(out_file, "w") as f:
        Hyperparams.print_title(f)
    for hyperparam in hyperparams:
        hyperparam.run()
        with open(out_file, "a") as f:
            hyperparam.print(f)
        best = max(hyperparams, key=Hyperparams.score)
        print("Best hyperparams: %s" % best)


if __name__ == "__main__":
    main()
