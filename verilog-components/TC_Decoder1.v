module TC_Decoder1 (sel, out);
    input sel;
    output reg [1:0] out;

    always @ (sel)
    begin
        case(sel)
        1'b0 : out <=  2'b01;
        1'b1 : out <=  2'b10;
        endcase
    end 
endmodule

