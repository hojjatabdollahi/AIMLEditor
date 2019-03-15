import Utils.Storage as Storage
from Model.Data import *


# create AIML structure
aiml = AIML().append(
    Category().append(
        Pattern().append("START SESSION 1 *")
    ).append(
        Template().append(
            Think().append(
                Set("username").append("star")
            ).append(
                Set("topic").append("Session 1")
            )
        ).append("Ok. Let's begin our session. How are you doing today <star/>?").append(
            Oob().append(Robot())
        )
    )
).append(
    Topic("session").append(
        Category().append(
            Pattern().append("*")
        ).append(
            Template().append(
                Think().append(Set("data").append("<star/>"))
            ).append(
                Condition("getsetimnet").append(
                    ConditionItem("verypositive").append("I am happy").append(
                        Oob().append(
                            Robot().append(
                                Options().append(
                                    Option("Yes")
                                ).append(
                                    Option("No")
                                )
                            )
                        )
                    )
                ).append(
                    ConditionItem("positive").append(
                        "I am not as happy")
                )
            )
        )
    )
)
# print it as a reference
print(aiml)


Storage.save('test2', aiml)  # save as a pickle file
aiml2 = Storage.restore('test2')  # restore the pickle
print("####################restored pickle file#######################")
print(aiml2)  # print for validation

Storage.exportAIML('test2', aiml2)  # save as an aiml file
aiml4 = Storage.importAIML('test2')  # import the aiml file
print(aiml4)  # print for validation
