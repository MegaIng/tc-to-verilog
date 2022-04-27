module TC_Switch1(en, in, out);
    input en;
    input in;
    tri0 reg out;
    
    always @ (en or in) begin
        case(en)
        1'b0 : out <= 1'bZ;
        1'b1 : out <= in;
        endcase
    end
endmodule

