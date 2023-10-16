# helix.personmatching

<p align="left">
  <a href="https://github.com/icanbwell/helix.personmatching/actions">
    <img src="https://github.com/icanbwell/helix.personmatching/workflows/Build%20and%20Test/badge.svg"
         alt="Continuous Integration">
  </a>
  <a href="https://github.com/icanbwell/helix.personmatching/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202-blue"
         alt="GitHub license">
  </a>
</p>

## Entrypoint
[helix_personmatching/matchers/matcher.py](helix_personmatching/matchers/matcher.py)

## Inputs
This code takes in:
1. A source Patient/Person resource or a Bundle of Patient/Person resources
2. A target Patient/Person resource or a Bundle of Patient/Person resources
3. A set of rule options/weights
4. Whether to return only successful matches or all match results
5. (Optional) Matching threshold (between 0 and 1).  Can also be set as an environment variable: `PERSON_MATCH_THRESHOLD`
6. (Optional) Average score boost (between 0 and 1).  Can also be set as an environment variable: `PERSON_MATCH_AVERAGE_SCORE_BOOST`


## Outputs
1. A list of match results where id_source is id of source record and id_target is id of matched record.

# Logic
1. The code runs through each rule and calculates a uniqueness probability (between 0 and 1) if the rule matches.
2. The code then picks the rule with the highest uniqueness probability and uses that probability
3. The code then calculates the average of all the other rule probabilities and boosts the uniqueness probability by it.
4. The code then sees if any other boosting rules were requested and boosts the probability by those

# Weights
There are five cases when matching fields of two records in a rule and the weights that are applied for each case:
1. Field present in both sides and match -> `exact_match`
2. Field present in both sides and partial match -> `partial_match`
3. Field missing in both sides -> `missing`
4. Field missing in one side -> `missing`
5. Field present in both sides but do not match -> 0.0

For boosting rules, there is an additional `boost` weight.

