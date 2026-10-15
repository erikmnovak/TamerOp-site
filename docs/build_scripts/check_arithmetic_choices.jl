# Check the website's prepared arithmetic examples against the library.
import TamerOp as OP
import JSON3
using Test

const A = OP.Advanced
const FL = OP.FieldLinAlg
cases = JSON3.read(read(ARGS[1], String))

@testset "Prepared arithmetic choices" begin
    @testset "Numerical cutoff and exact rank" begin
        matrix = [1.0 0.0; 0.0 1e-14]
        exact = OP.QQ[1 0; 0 1//big(10)^14]
        @test FL.rank(OP.CoreModules.QQField(), exact) == 2
        for state in cases.cutoff
            field = OP.CoreModules.RealField(Float64; atol=Float64(state.atol), rtol=0.0)
            @test FL.rank(field, matrix; backend=:float_dense_svd) == state.rank
            @test size(FL.nullspace(field, matrix; backend=:float_dense_svd), 2) == state.nullity
        end
    end
    @testset "Exact candidate and membership certificate" begin
        field = OP.CoreModules.QQField()
        B = OP.QQ[1 2; 2 4; 0 1]
        factor = FL.factor_fullcolumn(field, B; backend=:julia_exact, cache=false)
        for state in cases.certificate
            y = OP.QQ[1, state.y2, -1]
            candidate = OP.QQ[3, -1]
            @test B * candidate - y == OP.QQ[0, state.residual, 0]
            if state.accepted
                @test FL.solve_fullcolumn(field, B, y; factor, backend=:julia_exact) == candidate
            else
                @test_throws ErrorException FL.solve_fullcolumn(field, B, y; factor, backend=:julia_exact)
            end
        end
    end
    @testset "Closed segment and neighboring zero spaces" begin
        options = A.EncodingOptions(; backend=:pl_backend, poset_kind=:signature,
                                    field=OP.CoreModules.QQField())
        segment = OP.encode([A.BoxUpset([0, 0])], [A.BoxDownset([0, 2])], OP.QQ[1;;], options)
        M, pi = OP.encoding_module(segment), OP.encoding_map(segment)
        for state in cases.boundary
            q = (OP.QQ(state.x), OP.QQ(state.y))
            @test A.dim_at(M, A.locate(pi, q)) == state.dimension
            @test collect(state.signature) == [Int(q[1] >= 0 && q[2] >= 0), Int(q[1] > 0 || q[2] > 2)]
        end
    end
    @testset "Exact radii with coincident floating displays" begin
        delta = OP.QQ(1, big(2)^70)
        source = OP.PointCloud(reshape(OP.QQ[0, 2, 4 + delta], :, 1))
        enc = OP.encode(source, OP.RhomboidFiltration(); degree=0)
        M, pi = OP.encoding_module(enc), OP.encoding_map(enc)
        first, second = OP.AlgebraicReal(1), OP.AlgebraicReal(1 + delta/2)
        @test first < second
        @test Float64(first) == Float64(second) == 1.0
        for state in cases.grades
            r = OP.AlgebraicReal(1 + OP.QQ(state.offset, big(2)^state.power))
            @test Float64(r) == (state.id == "before" ? 0.5 : 1.0)
            @test A.dim_at(M, A.locate(pi, (r, OP.AlgebraicReal(1)))) == state.components
        end
    end
end
