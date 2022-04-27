module TC_Mux8(sel, a, b, out);
    input sel;
    input [7:0] a;
    input [7:0] b;
    output reg [7:0] out;
    
    always @ (sel or a or b) begin
        case(sel)
        1'b0 : out <= a;
        1'b1 : out <= b;
        endcase
    end
endmodule

