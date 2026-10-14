#!/usr/bin/env julia
# Execute the canonical rectangle example and derive its displayed witness.
module ExactMatchingGuide
const PAGE = normpath(joinpath(@__DIR__, "..", "exact_matching.md"))
const FIGURE = normpath(joinpath(@__DIR__, "..", "assets", "exact_matching", "witness.svg"))
function check(; render=false)
    source = read(PAGE, String)
    start = "<!-- BEGIN exact_matching_example -->"
    stop = "<!-- END exact_matching_example -->"
    part = split(split(source, start; limit=2)[2], stop; limit=2)[1]
    blocks = collect(eachmatch(r"```julia\n(.*?)\n```"s, part))
    length(blocks) == 2 || error("Expected construction and exact witness blocks")
    workspace = Module(:ExactMatchingExample)
    figure = nothing
    for (i, block) in enumerate(blocks)
        println("Executing exact matching example block $i"); flush(stdout)
        figure = Base.include_string(workspace, block.captures[1], "exact_matching.md:block-$i")
    end
    if render
        Cairo = Base.invokelatest(getfield, workspace, :CairoMakie)
        Base.invokelatest(() -> Cairo.save(FIGURE, figure))
        println("Rendered $FIGURE")
    end
    println("Exact matching example agrees with the proved bound and optimizing line.")
    return (;workspace, figure)
end
end
if abspath(PROGRAM_FILE) == @__FILE__
    all(==("--render"), ARGS) || error("Usage: check_exact_matching.jl [--render]")
    ExactMatchingGuide.check(;render="--render" in ARGS)
end
