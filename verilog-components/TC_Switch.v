module TC_Switch(en, in, out);
    parameter size = 1;
    input en;
    input [size-1:0] in;
    output tri0 reg [size-1:0] out;
    
    always @ (en or in) begin
        case(en)
        1'b0 : out <= {size{1'bZ}};
        1'b1 : out <= in;
        endcase
    end
endmodule

