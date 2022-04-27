module TC_Mux64(sel, in0, in1, out);
    input sel;
    input [63:0] in0;
    input [63:0] in1;
    output reg [63:0] out;
    
    always @ (sel or in0 or in1) begin
        case(sel)
        1'b0 : out <= in0;
        1'b1 : out <= in1;
        endcase
    end
endmodule

