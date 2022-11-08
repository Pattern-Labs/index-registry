# Index Registry Tools
This is an initial readme for the Index Registry Tools which may change and I probably wont cover everything here.
Mainly used to discus the implementation of our bazel managment system.

## Bazel Version Management
In order to manage bazel management there are two main things each with potentially a couple way of implementing.
1. ***Bazel Tools:*** These are the bazel tools needed to manage updating versions, updating tags as well as understanding/parsing
the contents of a `MODULE.bazel` file. These have all been implemented and are waiting for further testing. THey have been tested
on example cases however will also need testing in real world application. These tools should be agnostic of the later portion
of the management system. The tools are all implemented in python with github workflow calls that can invoke them.
1. ***Version Mangement***: The key portion of this project is to handle dependency managment of all bazel based modules in
the pattern organization. This means that the bazel verseion management system needs to be able to handle updating the 
dependents of a module in the case of a module being updated. This is where the contrversy around implementation arises
which I will proceed to outline in the following implementation methods.
     1. ***Handle Bazel Dependencies in the Index Registry:*** If we were going to handle bazel dependencies inside of the index
     registry it would mean that we have all repos with bazel modules inside of the index registry regardless of whether they
     have things that are dpendent on them. This would mean that we would put things like apollo and prototype controller inside
     of it even tho they are not currently in there. I Like this method a lot because it means that everything is centralized and
     resolving dependencies can be done from one python function call. The modules that need to be updated can be set ot an
     environment variable which can can then be used to trigger multiple actions from it.

          Pros:
                
                * Everything is in one space
                * Simpler workflows
            
          Cons:
                
                * You have to add some modules that you would not otherwise have to.
     1. ***Handle Bazel Dependencies outside of the Index Registry:***This method would mean that some modules (ie. apollo, prototype-controler, etc.)
     would not be housed in the index registry. Since not everything is handled in the index registry, I would implement this as if nothing was housed
     in the index registry. I dont want to add additional cases or specific lists of repos that need special treatment because I do not believe this 
     would scale. This would mean that you would have to checkout every pattern repo and then check if it is a bazel module and then if it is you
     would need to manage it.
          
          pros:
          
              * You dont have to put modules like apollo and prototype controller in the repo
          
          cons:
              * Requires a bunch of checking out of repos with unkown tags which means that things could get out of sync.
