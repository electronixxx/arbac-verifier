# Arbac Verification Challenge - Security II
This simple script can be used to verify the reachability of simple ARBAC rules. It is composed
of a parser which parses an .arbac file written into a specific form (as explained
in the description pdf), and saves all it’s elements into adeguate data structures.

Once the parsing is done, the analyzer starts analyzing the reachability of the target role.
First it executes the forward and backward slicing on the initial parsed
data in order to reduce the state space.

It is developed for the purpose of solving the third challenge of the
Security 2 course. In roughly 5 minutes it finds the reachabilities for all the 8
policies of the challenge, and so, obtain the flag as the concatenation of the
reachabilities expressed as zero or one.

## Author
Hernest Serani - Matricola 877028

Security II - 2021/2022

Ca' Foscari University of Venice

## Implementation
A detailed report can be found [here](docs/report.pdf).

## Output
The output shows the state of the execution for each of the input policy. Furthermore it gives
details about the made reductions (using prunning algorithms) and the time of execution.


```{bash}
----------------------------------------------------------------------------------------------------------
Testing reachability of policy1.arbac
Forward and Backward slicing applied. Reductions made: [Nr Roles by 8] | [CA Rules by 8] | [CR Rules by 5]
Number of states reduced from 1427247692705959881058285969449495136382746624 to 1180591620717411303424
Role reachable. Found in 5.176304801000697 seconds.
----------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------
Testing reachability of policy2.arbac
Forward and Backward slicing applied. Reductions made: [Nr Roles by 10] | [CA Rules by 10] | [CR Rules by 10]
Number of states reduced from 1427247692705959881058285969449495136382746624 to 1125899906842624
Role not reachable. Found in 9.271649135000189 seconds.
----------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------
Testing reachability of policy3.arbac
Forward and Backward slicing applied. Reductions made: [Nr Roles by 9] | [CA Rules by 10] | [CR Rules by 5]
Number of states reduced from 1427247692705959881058285969449495136382746624 to 1152921504606846976
Role reachable. Found in 0.07023365900022327 seconds.
----------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------
Testing reachability of policy4.arbac
Forward and Backward slicing applied. Reductions made: [Nr Roles by 6] | [CA Rules by 6] | [CR Rules by 5]
Number of states reduced from 1427247692705959881058285969449495136382746624 to 1237940039285380274899124224
Role reachable. Found in 0.012380957000459603 seconds.
----------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------
Testing reachability of policy5.arbac
Forward and Backward slicing applied. Reductions made: [Nr Roles by 8] | [CA Rules by 8] | [CR Rules by 6]
Number of states reduced from 1427247692705959881058285969449495136382746624 to 1180591620717411303424
Role not reachable. Found in 132.69451744199978 seconds.
----------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------
Testing reachability of policy6.arbac
Forward and Backward slicing applied. Reductions made: [Nr Roles by 8] | [CA Rules by 8] | [CR Rules by 6]
Number of states reduced from 1427247692705959881058285969449495136382746624 to 1180591620717411303424
Role reachable. Found in 0.004751634000058402 seconds.
----------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------
Testing reachability of policy7.arbac
Forward and Backward slicing applied. Reductions made: [Nr Roles by 7] | [CA Rules by 7] | [CR Rules by 3]
Number of states reduced from 1427247692705959881058285969449495136382746624 to 1208925819614629174706176
Role reachable. Found in 0.5332487870000477 seconds.
----------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------
Testing reachability of policy8.arbac
Forward and Backward slicing applied. Reductions made: [Nr Roles by 8] | [CA Rules by 8] | [CR Rules by 5]
Number of states reduced from 1427247692705959881058285969449495136382746624 to 1180591620717411303424
Role not reachable. Found in 127.12636846799978 seconds.
----------------------------------------------------------------------------------------------------------



Flag: 10110110 found in 274.9355365849997 seconds.

```