@tag_name_1 @tag_name_n <optional>
Feature: <descriptive title>

  As a <user>
  I want to <do something | need something>
  So that <I can achieve something>
 
  Contributes to <agile requirement artefact category> <filename or title of the artefact> <(optional in case the contribution is to an artefact that is detailed with rules) using rule <rule as it is formulated>   

  Description (optional): <further optional description to understand
  the rule, no format defined, the example artefact is only a placeholder>

  Background:
    Given <what is given for all scenarios in this feature file>

  Rule: <points to a specific rule which is valid for the next set of scenarios until the next rule is given>  
  Scenario: <descriptive scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

  Scenario: <another descriptive scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

  Rule: <points to another specific rule which is valid for the next set of scenarios until the next rule is given>  
  Scenario Outline: <descriptive scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

    Examples:
      | descriptive scenario title | precondition | action  | expected result |
      | <example title 1>          | <example precond. 1> | <example action 1> | <example result 1> |
      | <example title 2>          | <example precond. 2> | <example action 2> | <example result 2> |
