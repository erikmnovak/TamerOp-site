using Pkg
using TOML

# The two projects have independent environments. Only this generated environment
# points to a local library checkout; the authored Project.toml stays unchanged.
docs = @__DIR__
library = realpath(get(ENV, "TAMEROP_SOURCE", joinpath(docs, "..", "..", "TamerOp.jl")))
package = TOML.parsefile(joinpath(library, "Project.toml"))
package["name"] == "TamerOp" || error("TAMEROP_SOURCE must identify a TamerOp checkout")
package["uuid"] == "40830518-3340-46e0-bdcb-56edef4036ff" || error("Unexpected TamerOp UUID")
environment = joinpath(docs, ".build", "environment")
mkpath(environment)
project = TOML.parsefile(joinpath(docs, "Project.toml"))
project["sources"] = Dict("TamerOp" => Dict("path" => library))
open(joinpath(environment, "Project.toml"), "w") do io
    TOML.print(io, project; sorted=true)
end
Pkg.activate(environment)
# resolve() does not install a registry in a fresh Julia depot. This is a
# no-op when General is already installed, including ordinary local builds.
Pkg.Registry.add("General")
Pkg.resolve()
Pkg.instantiate()
println("Website environment: ", environment)
println("TamerOp checkout: ", library)
