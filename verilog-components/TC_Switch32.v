module TC_Switch32(en, in, out);
    input en;
    input [31:0] in;
    tri0 reg [31:0] out;
    
    always @ (en or in) begin
        case(en)
        1'b0 : out <= 32'bZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ_ZZZZ;
        1'b1 : out <= in;
        endcase
    end
endmodule

