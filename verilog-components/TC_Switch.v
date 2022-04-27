module TC_Switch(en, in, out);
    parameter size = 1;
    input en;
    input [size-1:0] in;
    output tri0 [size-1:0] out;
	 reg [size-1:0] outval;
    
    always @ (en or in) begin
        case(en)
        1'b0 : outval = {size{1'bZ}};
        1'b1 : outval = in;
        endcase
    end
	 assign out = outval;
endmodule

