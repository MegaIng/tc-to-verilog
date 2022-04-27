module TC_Mux(sel, in0, in1, out);
    parameter size = 1;
    input sel;
    input [size-1:0] in0;
    input [size-1:0] in1;
    output reg [size-1:0] out;
    
    always @ (sel or in0 or in1) begin
        case(sel)
        1'b0 : out <= in0;
        1'b1 : out <= in1;
        endcase
    end
endmodule

