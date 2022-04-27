module TC_Switch(sel, in, out);
    parameter size = 1;
    input sel;
    input [size-1:0] in;
    tri0 reg [size-1:0] out;
    
    always @ (en or in) begin
        case(en)
        1'b0 : out <= {size{1'bZ}};
        1'b1 : out <= in;
        endcase
    end
endmodule

