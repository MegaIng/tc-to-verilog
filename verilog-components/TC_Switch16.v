module TC_Switch16(en, in, out);
    input en;
    input [15:0] in;
    tri0 reg [15:0] out;
    
    always @ (en or in) begin
        case(en)
        1'b0 : out <= 16'bZZZZ_ZZZZ_ZZZZ_ZZZZ;
        1'b1 : out <= in;
        endcase
    end
endmodule

