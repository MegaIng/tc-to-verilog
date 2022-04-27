module TC_Switch64(en, in, out);
    input en;
    input [63:0] in;
    tri0 reg [63:0] out;
    
    always @ (en or in) begin
        case(en)
        1'b0 : out <= 64'bZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ;
        1'b1 : out <= in;
        endcase
    end
endmodule

